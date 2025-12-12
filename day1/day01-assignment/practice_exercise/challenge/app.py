from services.weather_service import get_weather

API_KEY = "55b72adc787cfa62423cb0e6bad4e21a"

city = input("Enter city: ")
data = get_weather(city, API_KEY)

print("Weather data for", city)
print("Temperature:", data["main"]["temp"], "°C")
print("Humidity:", data["main"]["humidity"], "%")
print("Description:", data["weather"][0]["description"])