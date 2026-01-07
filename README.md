Singidunum University  
AAI – Cloud Computing and Software Development  

lab_Weather_App_CC_SD_2025

• Micro web application using Open-Meteo (https://open-meteo.com/)  
• Public URL showing weather data for two cities and last update time  
• Data persists in SQLite (survives app restarts)  
• Application runs as a systemd service, fronted by Apache reverse proxy  

Tools

• Azure Portal  
• Windows Terminal / SSH  
• SQLite  
• ChatGPT  

---

Run locally (without VM)

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install Flask

export SECRET_KEY=dev            # Windows: set SECRET_KEY=dev
python app/app.py

Open in browser:
http://127.0.0.1:5000/
http://127.0.0.1:5000/admin/sync
http://127.0.0.1:5000/api/weather?city=Belgrade

---

Production (Azure VM)

• Flask runs on port 5000 as a systemd service  
• Apache reverse proxy exposes the app on port 80  
• Apache and systemd configuration files are versioned in infra/  

---

Project structure

app/            Flask application  
infra/apache/   Apache reverse proxy configuration  
infra/systemd/  systemd service file  
