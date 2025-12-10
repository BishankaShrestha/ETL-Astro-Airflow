ETL Weather Pipeline using Apache Airflow & Dockerized Postgres

This project is a simple ETL (Extract–Transform–Load) pipeline built using Apache Airflow, HTTP Hook, and Postgres Hook.
The pipeline fetches real-time weather data from the Open-Meteo API and stores it in a Postgres database running inside Docker.

🚀 Architecture Overview
Airflow DAG Scheduler
|

---

| | |
Extract Transform Load
(HTTP API) (JSON) (Postgres Hook)
| |
-------------> Docker Postgres

📡 Extract – HTTP Hook

Airflow connects to Open-Meteo API using a configured HTTP connection:

Host stored in Airflow Conn: https://api.open-meteo.com

Endpoint handled in code:

/v1/forecast?latitude=...&longitude=...&current_weather=true

🔄 Transform

We extract only:

Temperature

Wind speed

And convert them into a simple Python dictionary.

🗄️ Load – Postgres Hook

Postgres is running inside Docker.
Airflow connects using:

Host: postgres
User: postgres
Password: postgres
DB: postgres
Port: 5432

The DAG:

Creates the table if it doesn’t exist

Inserts the latest weather data

🐳 Docker Setup (Postgres Database)
version: "3"
services:
postgres:
image: postgres:13
container_name: postgres_db
environment:
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: postgres
ports: - "5432:5432"
volumes: - postgres_data:/var/lib/postgresql/data

volumes:
postgres_data:

Start Postgres:

docker-compose up -d

🪝 Airflow DAG Code

Your full DAG code is inside:

dags/etl_weather_pipeline.py

⚙️ Airflow Connections Required

1. HTTP Connection
   Conn ID: open_meteo_api
   Conn Type: HTTP
   Host: https://api.open-meteo.com

2. Postgres Connection
   Conn ID: postgres_default
   Conn Type: Postgres
   Host: postgres
   User: postgres
   Password: postgres
   Port: 5432
   Schema: postgres

▶️ Running the ETL Pipeline (Astro CLI)

Initialize:

astro dev init

Start Airflow:

astro dev start

Restart if needed:

astro dev restart

Open Airflow UI:

http://localhost:8080

Trigger the DAG manually or wait for schedule.

📊 Check Stored Data

Use:

docker exec -it postgres_db psql -U postgres -d postgres
SELECT \* FROM weather_data;

📦 Requirements

requirements.txt:

apache-airflow-providers-http
apache-airflow-providers-postgres

🎯 Future Improvements

Add timestamps

Add error handling & retries

Store historical data

Use Airflow Variables for config

Add Grafana dashboard
