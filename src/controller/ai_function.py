from fastapi import HTTPException
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from src.tools import get_weather

def ask_question(question: str):
    try:
        llm = ChatGroq(
                       model="llama-3.3-70b-versatile",
                       temperature=0.8,
                       timeout=30,
                       max_tokens=1000,
                       max_retries=8,  # Default; increase for unreliable networks
                       )
        tools = [get_weather]
        agent = create_agent(llm, tools=tools)

        print("--- Calling the Agent ---")
        query = question
        response = agent.invoke({"messages": [("user", query)]})
        
        print("\n--- Final Answer ---")
        print(response["messages"][-1].content)
        # This extracts just the final text answer from the agent
        # Replace your current return statement with this:
        return {
    "yourQuistion": question, 
    "response": response["messages"][-1].content
}
    except Exception as e :
        raise HTTPException(status_code=500,detail= f"error is this {str(e)}")

 
