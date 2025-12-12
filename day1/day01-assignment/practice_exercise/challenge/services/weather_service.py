import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, api_key):
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    return response.json()
