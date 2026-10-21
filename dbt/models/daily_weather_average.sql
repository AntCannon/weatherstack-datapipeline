{{ config(materialized='view') }}

SELECT
  city,
  cast(weather_time_local AS date) as weather_date,
  round(avg(temperature)::numeric, 2) as avg_temperature,
  round(avg(wind_speed)::numeric, 2) as avg_wind_speed,
  count(*) as observation_count
FROM {{ ref('stg_weather_data')}}
GROUP BY
  city,
  cast(weather_time_local as date)