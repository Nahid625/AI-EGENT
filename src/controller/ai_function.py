from langchain_groq import ChatGroq
from fastapi import HTTPException
from src.tools import get_weather, gettime
from langchain_community.tools import DuckDuckGoSearchRun
from groq import Groq
import base64


def ask_question(question: str, history: list = []) -> str:

    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, timeout=30)
        question_lower = question.lower()

        # build messages with history
        messages = history + [{"role": "user", "content": question}]

        if any(word in question_lower for word in ["time", "clock"]):
            tz_response = llm.invoke(f"Extract timezone in pytz format from: {question}. Return ONLY timezone.")
            timezone = tz_response.content.strip()
            return gettime.invoke({"timezone": timezone})

        elif any(word in question_lower for word in ["weather", "temperature", "humid"]):
            city_response = llm.invoke(f"Extract city name from: {question}. Return ONLY city name.")
            city = city_response.content.strip()
            return get_weather.invoke({"location": city})

        elif any(word in question_lower for word in ["news", "latest", "today", "current", "now", "age", "old", "born"]):
            search = DuckDuckGoSearchRun()
            result = search.invoke(question)
            summary = llm.invoke(f"Based on this search result, answer '{question}':\n\n{result}")
            return summary.content

        else:
            response = llm.invoke(messages)   # ← pass full history here ✅
            return response.content

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


groq_client = Groq()

def ask_with_image(question: str, image_file) -> str:
    try:
        # Convert image to base64
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # ← vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                }
            ],
            max_tokens=1024
        )
        return response.choices[0].message.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))