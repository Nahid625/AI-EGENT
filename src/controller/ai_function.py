from langchain_groq import ChatGroq
from fastapi import HTTPException
from src.tools import get_weather, gettime
from langchain_community.tools import DuckDuckGoSearchRun

def ask_question(question: str) -> dict:
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            timeout=30
        )

        question_lower = question.lower()

       
        
        
        # Time question
        if any(word in question_lower for word in ["time", "clock"]):
            # Ask LLM to extract timezone from question
            tz_response = llm.invoke(
                f"Extract the timezone in pytz format (like 'Asia/Dhaka', 'America/New_York') from this question. Return ONLY the timezone string, nothing else: {question}"
            )
            timezone = tz_response.content.strip()
            result = gettime.invoke({"timezone": timezone})
            return {"yourQuistion": question, "response": result}

        # Weather question
        elif any(word in question_lower for word in ["weather", "temperature", "humid"]):
            # Ask LLM to extract city name
            city_response = llm.invoke(
                f"Extract only the city name from this question. Return ONLY the city name, nothing else: {question}"
            )
            city = city_response.content.strip()
            result = get_weather.invoke({"location": city})
            return {"yourQuistion": question, "response": result}

        # News / live search
        elif any(word in question_lower for word in ["news", "latest", "today", "current", "now"]):
            search = DuckDuckGoSearchRun()
            result = search.invoke(question)
            # Let LLM summarize the search result
            summary = llm.invoke(f"Based on this search result, answer the question '{question}':\n\n{result}")
            return {"yourQuistion": question, "response": summary.content}

        # Everything else — direct LLM answer
        else:
            response = llm.invoke(question)
            return {"yourQuistion": question, "response": response.content}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))