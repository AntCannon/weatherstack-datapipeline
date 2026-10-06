import os
from dotenv import load_dotenv
import psycopg2
import api_request

load_dotenv()

# db configuration
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

target_function_name = "get_mock_weather_data"
target_function = getattr(api_request, target_function_name)
target_data = target_function()


def connect_to_db():
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )
        print("Connected to the database successfully.")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise


def create_table(conn):
    print("Creating table if it doesn't exist...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_descriptions TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT,
                sunrise TEXT,
                sunset TEXT
            );
        """)
        conn.commit()
        print("Table was created.")

    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise


conn = connect_to_db()
create_table(conn)
