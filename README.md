# Weather ETL Pipeline with Apache Airflow

A production-ready ETL (Extract, Transform, Load) pipeline built with Apache Airflow that fetches real-time weather data from the OpenMeteo API and stores it in a PostgreSQL database.

## Overview

This project demonstrates a complete ETL workflow that:
- **Extracts** current weather data (temperature and wind speed) from the OpenMeteo API for London
- **Transforms** the raw API response into a structured format
- **Loads** the processed data into a PostgreSQL database

The pipeline runs daily and is orchestrated using Apache Airflow with the TaskFlow API.


## Features

- **Automated daily weather data collection**
- **Modular design** using Airflow's TaskFlow API decorators
- **Error handling** for API failures
- **Docker-based** PostgreSQL database
- **Connection management** via Airflow connections
- **Idempotent operations** with table creation checks

## Prerequisites

- Python 3.8+
- Apache Airflow 2.0+
- Docker & Docker Compose
- Astronomer CLI (optional, for local development)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd weather-etl-pipeline
```

### 2. Start PostgreSQL Database

```bash
docker-compose up -d
```

This will start a PostgreSQL container with:
- **Host:** localhost
- **Port:** 5432
- **Database:** postgres
- **User:** postgres
- **Password:** postgres

### 3. Install Airflow Dependencies

If using Astronomer:
```bash
astro dev start
```

Or install manually:
```bash
pip install apache-airflow
pip install apache-airflow-providers-http
pip install apache-airflow-providers-postgres
```

### 4. Configure Airflow Connections

#### PostgreSQL Connection
Navigate to **Admin → Connections** in the Airflow UI and create:

- **Connection ID:** `postgres_default`
- **Connection Type:** Postgres
- **Host:** `postgres` (or `localhost` if running Airflow outside Docker)
- **Schema:** `postgres`
- **Login:** `postgres`
- **Password:** `postgres`
- **Port:** `5432`

#### OpenMeteo API Connection
- **Connection ID:** `open_meteo_api`
- **Connection Type:** HTTP
- **Host:** `https://api.open-meteo.com`

### 5. Enable and Trigger the DAG

1. Open the Airflow UI (typically at `http://localhost:8080`)
2. Find the `etl_weather_pipeline` DAG
3. Toggle it to "On"
4. Click "Trigger DAG" to run manually or wait for the daily schedule

## 📂 Project Structure

```
.
├── dags/
│   └── etl_weather_pipeline.py    # Main ETL DAG definition
└── README.md                       # Project documentation
```

## 🔧 Configuration

### Location Settings
To change the weather data location, modify these constants in `etl_weather_pipeline.py`:

```python
LATITUDE = '51.5074'   # London latitude
LONGITUDE = '-0.1278'  # London longitude
```

### Schedule
The DAG runs daily by default. Modify the schedule in the DAG definition:

```python
schedule = '@daily'  # Can be changed to '@hourly', '0 0 * * *', etc.
```

## Database Schema

The pipeline creates a `weather_data` table with the following structure:

| Column      | Type  | Description              |
|-------------|-------|--------------------------|
| temperature | FLOAT | Temperature in Celsius   |
| windspeed   | FLOAT | Wind speed in km/h       |

##  DAG Tasks

1. **extract_weather_data**: Fetches current weather data from OpenMeteo API
2. **transform_weather_data**: Extracts temperature and wind speed from the response
3. **load_into_database**: Inserts transformed data into PostgreSQL

## Troubleshooting

### Connection Errors
- Verify PostgreSQL is running: `docker ps`
- Check Airflow connections are configured correctly
- Ensure network connectivity between Airflow and PostgreSQL

### API Failures
- Check internet connectivity
- Verify the OpenMeteo API is accessible: `curl https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true`

### Database Issues
- Check PostgreSQL logs: `docker logs postgres_db`
- Verify credentials in Airflow connection
- Ensure the database accepts connections from Airflow

## Future Enhancements

- [ ] Add data validation and quality checks
- [ ] Implement historical data backfilling
- [ ] Add timestamps to weather records
- [ ] Include additional weather parameters (humidity, pressure, etc.)
- [ ] Create data visualization dashboard
- [ ] Add alerting for extreme weather conditions
- [ ] Implement data retention policies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## 👤 Author

**Owner:** Bishanka

##  Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [OpenMeteo API Documentation](https://open-meteo.com/en/docs)
- [Astronomer Documentation](https://docs.astronomer.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
