# import os
# from groq import Groq
# from dotenv import load_dotenv
# load_dotenv()


# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# client = Groq(api_key=os.environ.get(GROQ_API_KEY))
# models = client.models.list()

# for model in models.data:
#     print(model.id)
import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from src.models.models  import QuestionResponse
from fastapi import APIRouter,str

app = APIRouter()



load_dotenv()

@tool
def get_weather(location: str) -> str:
    """USE THIS TOOL EVERY TIME the user asks about weather or temperature. 
    This tool fetches LIVE data from the internet for a specific city."""
    
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

# Use a slightly higher temperature (0.1) so it's not too stiff
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

tools = [get_weather]
agent = create_agent(llm, tools=tools)

print("--- Calling the Agent ---")
# Be very specific in the prompt to trigger the tool
query = "What is the exact current temperature in Dhaka? Use your weather tool."
response = agent.invoke({"messages": [("user", query)]})

print("\n--- Final Answer ---")
print(response["messages"][-1].content)
print(response)

@app.post("/question",response_model= QuestionResponse)
def ask_question(question: str , ):
    
    return {"message": question}
