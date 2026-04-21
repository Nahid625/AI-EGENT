import os

from langchain.tools import tool
from langchain_classic import requests


@tool
def get_weather(location: str) -> str:
    """Use this tool ONLY to get the current weather or temperature for a specific city. 
     Input should be a city name (e.g., 'Dhaka')."""
    # This print will show up in your terminal if the AI actually uses the tool
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
