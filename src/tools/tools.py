import os
import requests
from datetime import datetime
import pytz
from langchain.tools import tool  

@tool
def get_weather(location: str) -> str:
    """Get current weather for a city. Input should be a city name like 'Dhaka'."""
    print(f"--- TOOL LOG: Fetching weather for {location} ---")
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The weather in {location} is {temp}°C with {desc}."
        else:
            return f"Error from API: {response.status_code}"
    except Exception as e:
        return f"Connection Error: {e}"

@tool
def gettime(timezone: str) -> str:
    """Get current time for a timezone. Input should be like 'Asia/Dhaka' or 'America/New_York'."""
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"Current time in {timezone} is {current_time}"
    except Exception as e:
        return f"Error: {str(e)}"