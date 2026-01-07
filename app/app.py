from flask import Flask, render_template, request, jsonify
import sqlite3, json, time, urllib.request
from config import DB_PATH, CITIES

app = Flask(__name__)

def q(sql, params=(), one=False):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.execute(sql, params)
    rows = cur.fetchall()
    con.commit(); con.close()
    return (rows[0] if rows else None) if one else rows

@app.route("/")
def home():
    rows = q("""
      SELECT c.name, wc.temp_c, wc.wind_kph, wc.condition_text, wc.updated_at
      FROM cities c
      LEFT JOIN (
        SELECT city_id, temp_c, wind_kph, condition_text, updated_at
        FROM weather_cache
        WHERE (city_id, updated_at) IN (
          SELECT city_id, MAX(updated_at) FROM weather_cache GROUP BY city_id
        )
      ) wc ON wc.city_id = c.id
      WHERE c.is_active=1
      ORDER BY c.name
    """)
    last = q("SELECT MAX(updated_at) as t FROM weather_cache", one=True)
    return render_template("index.html", rows=rows, last_updated=(last["t"] if last and last["t"] else None))

@app.route("/api/weather")
def api_weather():
    city = request.args.get("city","Belgrade")
    row = q("""
      SELECT c.name, wc.temp_c, wc.wind_kph, wc.condition_text, wc.updated_at
      FROM cities c
      JOIN weather_cache wc ON wc.city_id=c.id
      WHERE c.name=? ORDER BY wc.updated_at DESC LIMIT 1
    """, (city,), one=True)
    if not row: return jsonify({"error":"no data"}), 404
    return jsonify(dict(row))

@app.route("/admin/sync")
def admin_sync():
    for c in CITIES:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}&current_weather=true"
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read().decode())
        cur = data.get("current_weather", {})
        temp = cur.get("temperature"); wind = cur.get("windspeed"); cond = "—"
        # Store
        city_id = q("SELECT id FROM cities WHERE name=?", (c["name"],), one=True)["id"]
        q("""INSERT INTO weather_cache(city_id,observed_at,temp_c,wind_kph,condition_text,raw_json,updated_at)
             VALUES(?,?,?,?,?,?,?)""",
          (city_id, time.strftime("%Y-%m-%d %H:%M:%S"),
           temp, wind, cond, json.dumps(data),
           time.strftime("%Y-%m-%d %H:%M:%S")))
    return "OK"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
