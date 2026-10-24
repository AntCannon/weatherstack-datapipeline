{{ config(materialized='view') }}

SELECT
  id,
  city,
  temperature,
  weather_descriptions,
  wind_speed,
  time AS weather_time_local,
  inserted_at,
  utc_offset,
  sunrise,
  sunset
from {{ source('weather', 'raw_weather_data') }}