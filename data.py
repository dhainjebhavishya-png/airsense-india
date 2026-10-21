import requests
from datetime import date, timedelta
import os
import pandas as pd

URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WX_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_air(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm2_5,pm10",
        "past_days": 90,
        "timezone": "Asia/Kolkata",
    }
    response = requests.get(URL, params=params, timeout=20)
    js = response.json()
    df = pd.DataFrame(js["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    return df

def fetch_air(lat, lon):
        params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm2_5,pm10",
        "past_days": 90,
        "timezone": "Asia/Kolkata",
    }
        response = requests.get(URL, params=params, timeout=20)
        js = response.json()
        df = pd.DataFrame(js["hourly"])
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        return df

def fetch_weather(lat, lon):
        params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation",
        "past_days": 90,
        "timezone": "Asia/Kolkata",
    }
        response = requests.get(WX_URL, params=params, timeout=20)
        js = response.json()
        df = pd.DataFrame(js["hourly"])
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        df = df.rename(columns={
        "temperature_2m": "temp",
        "relative_humidity_2m": "humidity",
        "wind_speed_10m": "wind",
        "wind_direction_10m": "wind_dir",
    })
        return df

def get_data(lat, lon):
    os.makedirs("cache", exist_ok=True)
    path = f"cache/{lat}_{lon}.csv"
    try:
        air = fetch_air(lat, lon)
        weather = fetch_weather(lat, lon)
        df = air.join(weather)
        df.to_csv(path)
        source = "live"
    except Exception:
        df = pd.read_csv(path, index_col="time", parse_dates=True)
        source = "cache"
    return df, source
def _table(url, params):
    js = requests.get(url, params=params, timeout=60).json()
    df = pd.DataFrame(js["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")


def get_long_data(lat, lon, days=365):
    end = date.today() - timedelta(days=6)
    start = end - timedelta(days=days)
    common = {
        "latitude": lat,
        "longitude": lon,
        "start_date": str(start),
        "end_date": str(end),
        "timezone": "Asia/Kolkata",
    }

    air = _table(URL, {**common, "hourly": "pm2_5,pm10"})
    weather = _table(
        "https://archive-api.open-meteo.com/v1/archive",
        {**common, "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation"},
    )
    weather = weather.rename(columns={
        "temperature_2m": "temp",
        "relative_humidity_2m": "humidity",
        "wind_speed_10m": "wind",
        "wind_direction_10m": "wind_dir",
    })
    return air.join(weather)

if __name__ == "__main__":
    df, source = get_data(19.07, 72.99)
    print(source)
    print(df.shape)


