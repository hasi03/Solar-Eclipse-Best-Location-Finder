import openmeteo_requests
import numpy as np
import requests_cache
import pandas as pd
from retry_requests import retry

import matplotlib.pyplot as plt

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"

# FILEPATH: /home/hasi/Documents/weather.ipynb
# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below

def weather_data(lat, long, start_date, end_date, month, day):
    import datetime

    data = []
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    dates = dates[dates.month == month]
    dates = dates[dates.day == day]

    for date in dates:

        params = {
            "latitude": lat,
            "longitude": long,
            "start_date": date.strftime("%Y-%m-%d"),
            "end_date": date.strftime("%Y-%m-%d"),
            "hourly": ["rain", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
            "daily": "sunshine_duration",
            "timezone": "America/Chicago"
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_rain = hourly.Variables(0).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(1).ValuesAsNumpy()
        hourly_cloud_cover_low = hourly.Variables(2).ValuesAsNumpy()
        hourly_cloud_cover_mid = hourly.Variables(3).ValuesAsNumpy()
        hourly_cloud_cover_high = hourly.Variables(4).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )
        }
        hourly_data["rain"] = hourly_rain
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
        hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
        hourly_data["cloud_cover_high"] = hourly_cloud_cover_high

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        data.append(hourly_dataframe)

    # Concatenate all dataframes into a single dataframe
    all_data = pd.concat(data)

    return all_data


# Function to get the maximum cloud cover for a given time interval. The time interval is a list of hours. It uses weighted average to calculate 
#the maximum cloud cover where most recent years have more weight.
def max_cloud(df, time_interval, year_start=2019):
    
    df['date'] = pd.to_datetime(df['date'], format='%Y:%m:%d:%H:%M')
    filtered_df = df[(df['date'].dt.hour.isin(time_interval) & (df['date'].dt.year>=year_start))]
    df2 = filtered_df.groupby(filtered_df['date'].dt.year).max()
    weights = df2['date'].dt.year.values-2024
    weighted_avg = np.average(df2['cloud_cover'], weights=1/weights)
    return weighted_avg



