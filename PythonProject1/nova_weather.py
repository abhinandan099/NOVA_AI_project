import requests
from nova_tts import read_aloud

API_KEY = 'your_openweathermap_api_key'

def weather(city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] != 200:
            read_aloud("City not found, please try again.")
            return
        main = data["main"]
        temp = main["temp"]
        desc = data["weather"][0]["description"]
        weather_report = f"The temperature in {city} is {temp}°C with {desc}."
        print(weather_report)
        read_aloud(weather_report)
    except Exception as e:
        print("Weather API error:", e)
        read_aloud("Sorry, I couldn't fetch the weather right now.")


'''
import requests
from nova_tts import read_aloud

def weather(city):
    api_key = "your_openweather_api_key"  # Put your API key here
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]
        wind_speed = data["wind"]["speed"]

        report = f"Current temperature in {city} is {temp}°C with {weather_desc}. Humidity is {humidity}% and wind speed is {wind_speed} meters per second."
        print("Nova:", report)
        read_aloud(report)
    else:
        msg = "City not found, please try again."
        print("Nova:", msg)
        read_aloud(msg)
'''