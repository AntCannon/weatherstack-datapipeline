import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import json

# env configuration
load_dotenv()
api_key = os.getenv("API_KEY")


# API configuration
headers = {"Accept": "application/json, application/json; Charset=UTF-8"}
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=Philadelphia"


def get_mock_weather_data():
    file_path = Path(__file__).resolve().parent.parent / "data" / "weather_data.json"
    mock_weather_data = json.loads(file_path.read_text(encoding="utf-8"))
    return mock_weather_data


def write_to_file(data, filename="weather_data.json"):
    print(f"Writing {data} to {filename}...")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data written to {filename} successfully.")


def fetch_data(api_key=api_key, api_url=api_url, headers=headers):
    print("Fetching weather data...")

    # get data
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        weather_data = response.json()
        print(weather_data)
        # write data to file
        write_to_file(weather_data)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        # Write mock data to file in case of an error
        mock_weather_data = get_mock_weather_data()
        write_to_file(mock_weather_data)
        raise


# fetch_data()
