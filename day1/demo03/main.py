import requests

api_key = "55b72adc787cfa62423cb0e6bad4e21a"
city = input("Enter city name:")
try:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    print("Status Code:", response.status_code)
    weather_data = response.json()
    print("Weather Data:", weather_data)
    print("Temperature: ", weather_data["main"]["temp"])
    print("Humidity: ", weather_data["main"]["humidity"])
    print("Wind Speed: ", weather_data["wind"]["speed"])

except:
    print("Some error occured")