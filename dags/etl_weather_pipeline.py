from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task

from datetime import datetime, timedelta


LATITUDE = '51.5074'
LONGITUDE = '-0.1278'
POSTGRES_CONN_ID = 'postgres_default' 
API_CONN_ID = 'open_meteo_api'
default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days=1)

}
with DAG(dag_id = 'etl_weather_pipeline',
         default_args = default_args,
         schedule = '@daily',
         catchup = False) as dags:
    @task()
    def extract_weather_data():
        '''Extracting weather data from OpenMeteo API using Airflow connection'''
        #Use http hook to get connection details from airflow connection
        http_hook = HttpHook(http_conn_id = API_CONN_ID, method = 'GET')
        #Need for API endpoint
        #Base URL: https://api.open-meteo.com
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'


       #request via hhtp hook
        response = http_hook.run(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    @task()
    def transform_weather_data(weather_data):
        current_weather = weather_data['current_weather']
        transformed_data = {
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed']
        }
        return transformed_data

    @task()
    def load_into_database(transformed_data):
        '''Load transformed data into the database'''
        pg_hook = PostgresHook(postgres_conn_id = POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        #create table if it doesnt exist
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS weather_data(
            temperature FLOAT,
            windspeed FLOAT
            )
            """
        )
        cursor.execute("""INSERT INTO weather_data(temperature, windspeed) VALUES(%s, %s)
            """, (
                transformed_data['temperature'],
                transformed_data['windspeed']
            ))
        
        conn.commit()
        cursor.close()


    weather_data = extract_weather_data()
    transform_data = transform_weather_data(weather_data)
    load_into_database(transform_data)

