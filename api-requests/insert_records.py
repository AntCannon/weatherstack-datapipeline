import os
from dotenv import load_dotenv
import psycopg2
from api_request import get_mock_weather_data

load_dotenv()


# db configuration
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


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


def insert_records(conn, data):
    print("Inserting weather data into the database...")

    location = data["location"]
    weather = data["current"]
    astro = weather["astro"]

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO dev.raw_weather_data (
                city,
                temperature,
                weather_descriptions,
                wind_speed,
                time,
                inserted_at,
                utc_offset,
                sunrise,
                sunset
            ) VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s)
        """,
            (
                location["name"],
                weather["temperature"],
                weather["weather_descriptions"][0],
                weather["wind_speed"],
                location["localtime"],
                location["utc_offset"],
                astro["sunrise"],
                astro["sunset"],
            ),
        )

        conn.commit()
        print("Data sucsessfully inserted.")

    except psycopg2.Error as e:
        print(f"Error inserting data into the database: {e}")
        raise


def main():
    try:
        data = get_mock_weather_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn, data)

    except Exception as e:
        print(f"an error occurred during execution: {e}")

    finally:
        if "conn" in locals():
            conn.close()
            print("Database connection closed.")


# main()
