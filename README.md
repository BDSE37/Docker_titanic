# 🚢 Docker Titanic Project - BDSE37 Group 1

This project is the final assignment for the BDSE37 Data Engineering group. It provides a containerized Titanic survival prediction system using Docker, consisting of:

-   Flask backend API for survival prediction
-   MySQL database for Titanic datasets
-  An Nginx static website as frontend
-  Unified orchestration via Docker Compose

---

##  Project Structure

```bash
Docker_titanic_BDSE37_Group1/
├── db_mysql/             # MySQL setup scripts and CSV data import
├── flask_app/            # Flask REST API backend (e.g., /api/predict)
├── nginx/                # Nginx config and HTML frontend (static pages)
├── docker-compose.yaml   # Compose file for service orchestration
├── .env.example          # Sample env vars (DO NOT commit .env)
└── README.md             # You are here


