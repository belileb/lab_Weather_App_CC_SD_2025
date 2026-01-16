Singidunum University  
AAI – Cloud Computing and Software Development  

lab_Weather_App_CC_SD_2025  
Public URL: http://20.108.24.219/

<img width="546" height="337" alt="weather_dashboard" src="https://github.com/user-attachments/assets/4b71c54f-f306-4540-b3c0-80fe92110c93" />

• Micro web application using Open-Meteo (https://open-meteo.com/)  
• Public web page showing weather data for two cities and last update time  
• Data persists in SQLite (survives application restarts)  
• Application runs as a systemd service, fronted by Apache reverse proxy  

Tools

• Azure Portal  
• Windows Terminal / SSH  
• SQLite  
• ChatGPT  

---

Run locally (development only)

This project is primarily deployed on an Azure VM.  
For simple local testing of the Flask app:

pip install Flask  
python app/app.py  

Open:
http://127.0.0.1:5000/

---

Production (Azure VM)

• Flask runs on port 5000 as a systemd service  
• Apache reverse proxy exposes the application on port 80  
• Apache and systemd configuration files are versioned in infra/  

---

Project structure

app/            Flask application  
infra/apache/   Apache reverse proxy configuration  
infra/systemd/  systemd service file  
