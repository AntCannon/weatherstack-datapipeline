import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_key = os.getenv("API_KEY")
headers = {"Accept": "application/json, application/json; Charset=UTF-8"}
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=Philadelphia"

mock_json = {"city": "Philadelphia", "temperature": 75, "humidity": 60}


def write_to_file(data, filename="weather_data.json"):
    print(f"Writing data to {filename}...")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data written to {filename} successfully.")


def fetch_data(api_key=api_key, api_url=api_url, headers=headers, mock_json=mock_json):
    print("Fetching weather data...")

    # get data
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        data = response.json()
        print(response.json())
        # write data to file
        write_to_file(data)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        # Write mock data to file in case of an error
        write_to_file(mock_json)
        raise


fetch_data()
