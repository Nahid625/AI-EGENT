from langchain_classic.agents import AgentExecutor,create_tool_calling_agent
from fastapi import HTTPException
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import DuckDuckGoSearchRun  
from src.tools import get_weather,gettime

def ask_question(question: str) -> str:
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            timeout=30
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant.
You have access to these tools: web search, weather, and time.

STRICT RULES — follow exactly:
- ONLY use a tool when the user asks for one of these:
  * current time or date
  * current weather in a location
  * recent news or live data from the internet
- For ALL other questions, answer directly using your own knowledge.
- NEVER call a tool for general knowledge, math, definitions, coding, or advice.
- If unsure whether to use a tool, do NOT use it."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        tools = [DuckDuckGoSearchRun(), get_weather, gettime]

        agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=False,  # ← False so real error surfaces in logs
            max_iterations=3              # ← prevent infinite tool call loops
        )

        response = agent_executor.invoke({"input": question})
        return response["output"]         # ← return plain string, not a dict

    except Exception as e:
        print(f"Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))