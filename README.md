# 🚢 Docker Titanic Project - BDSE37 Group 1

This project is the final assignment for the BDSE37 Data Engineering group. It implements a Docker-based Titanic survival prediction system, consisting of:

-  A Flask backend API for survival prediction
-  A MySQL database for storing the Titanic dataset
-  An Nginx static site as the frontend interface
-  Docker Compose for multi-service orchestration

---

## 📁 Project Structure

```bash
Docker_titanic_BDSE37_Group1/
├── db_mysql/             # MySQL schema and CSV import scripts
├── flask_app/            # Flask REST API backend (e.g., /api/predict)
├── nginx/                # Nginx static HTML frontend and reverse proxy config
├── docker-compose.yaml   # Compose file for service orchestration
├── .env.example          # Example environment variables (DO NOT commit .env)
└── README.md             # This file
```

---

##  Team Roles & Responsibilities

| Member                         | Responsibility               | Description                                                                 |
|--------------------------------|-------------------------------|-----------------------------------------------------------------------------|
| 張書婷                         | Docker Compose Integration   | Created `docker-compose.yaml`, connected all services, and did Final Check |
| 黃品茹<br>揭芷羽<br>謝理心     | MySQL & Data Import           | Created SQL schema and imported Titanic CSV into MySQL                      |
| 葉品孝                         | Model & Flask API             | Developed the logistic regression model and `/api/predict` endpoint        |
| 藍昱昕<br>焦亞妗               | Nginx & Frontend              | Designed static HTML pages and configured reverse proxy                     |
| Everyone                       | Documentation & Presentation  | Co-authored project report and final presentation                           |

---

## 📦 Technologies Used

| Technology       | Version | Purpose                       |
|------------------|---------|-------------------------------|
| Python           | 3.10    | ML model and Flask API        |
| Flask            | 2.x     | RESTful backend API           |
| MySQL            | 8.x     | Data storage and querying     |
| Nginx            | 1.23+   | Static site and reverse proxy |
| Docker           | 24.x    | Containerization              |
| Docker Compose   | 2.x     | Service orchestration         |

---

## ⚙️ Setup Instructions

```bash
# 1️⃣ Clone the repository
git clone git@github.com:BDSE37/Docker_titanic.git
cd Docker_titanic_BDSE37_Group1/

# 2️⃣ Copy the example environment variables
cp .env.example .env
# Edit the .env file to match your configuration (e.g., MySQL root password)

# 3️⃣ Build and start all containers
docker compose up --build

# 4️⃣ Access the system
Frontend: http://localhost:8080  
API:      http://localhost:5000/api/predict
```

---

## 📊 Model Info

- **Training data**: `train.csv` from Kaggle Titanic dataset  
- **Selected features**: `Pclass`, `Sex`, `Age`, `SibSp`, `Parch`, `Fare`
- **Model type**: Logistic Regression
- **Validation accuracy**: ~79%

---

##  MySQL Table Schema

```sql
CREATE TABLE passengers (
    PassengerId INT PRIMARY KEY,
    Survived TINYINT,
    Pclass INT,
    Name VARCHAR(100),
    Sex VARCHAR(10),
    Age FLOAT,
    SibSp INT,
    Parch INT,
    Ticket VARCHAR(50),
    Fare FLOAT,
    Cabin VARCHAR(50),
    Embarked VARCHAR(5)
);
```

---

## .gitignore Rules

Files and folders excluded from Git tracking:

```gitignore
.env
*.csv
__pycache__/
```

---

## 📝 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it for educational or academic purposes.

---
