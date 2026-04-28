import os
import requests  # ✅ standard library
from langchain.tools import tool
from fastapi import HTTPException
from datetime import datetime
import pytz

@tool
def get_weather(location: str) -> str:
    """Use this tool ONLY to get the current weather or temperature for a specific city.
     Input should be a city name (e.g., 'Dhaka')."""
    print(f"--- TOOL LOG: Fetching real data for {location} ---")
    
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    try:
        response = requests.get(url) 
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The REAL weather in {location} is {temp}°C with {desc}."
        else:
            return f"Error from API: {response.status_code}. Check if your API Key is active."
    except Exception as e:
        return f"Connection Error: {e}"
    

@tool
def gettime(time: str) -> str:
    """Use this tool to get the time like the current time or anything else the user wants, including different cities' times."""
    try:
        if time == "current":
            current_time = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
            return f"The current time is {current_time}"
        else:
            # TO DO: implement the logic to get the time for a specific city or timezone
            pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")