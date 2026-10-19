import json
import math
import random
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def generate_mock_weather():
    # load template
    template_path = (
        Path(__file__).resolve().parent.parent / "data" / "weather_data.json"
    )

    data = json.loads(template_path.read_text(encoding="utf-8"))

    # generate city
    city = random.choice(
        [
            "MOCK Philadelphia",
            "MOCK New York",
            "MOCK Boston",
        ]
    )

    data["location"]["name"] = city
    data["request"]["query"] = f"{city}, United States of America"

    # generate time information
    now = datetime.now(ZoneInfo("America/New_York"))

    data["location"]["localtime"] = now.strftime("%Y-%m-%d %H:%M:%S")
    data["location"]["localtime_epoch"] = int(now.timestamp())
    data["location"]["utc_offset"] = str(now.utcoffset().total_seconds() / 3600)
    data["current"]["observation_time"] = now.astimezone(ZoneInfo("UTC")).strftime(
        "%I:%M %p"
    )

    # generate temperature in Celsius
    hour = now.hour + now.minute / 60 + now.second / 3600
    daily_cycle = math.cos(2 * math.pi * (hour - 15) / 24)
    temperature = 18 + 7 * daily_cycle + random.uniform(-2, 2)

    data["current"]["temperature"] = round(temperature, 1)

    # generate weather description
    condition = random.choice(["Clear", "Partly Cloudy", "Overcast", "Light Rain"])

    data["current"]["weather_descriptions"] = [f"MOCK {condition}"]

    return data


def write_mock_weather(output_path):
    data = generate_mock_weather()
    output_path = Path(output_path)

    output_path.write_text(json.dumps(data, indent=4), encoding="utf-8")

    print(f"Mock weather written to {output_path}")
    return data
