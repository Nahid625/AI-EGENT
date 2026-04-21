from fastapi import HTTPException
from langchain.agents import create_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_groq import ChatGroq

from src.tools import get_weather

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

def ask_question(question: str):
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0, # Keep it 0 so it doesn't get "creative" and skip tools
            timeout=30
        )

        # FIX 1: Use a proper ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI agent. You HAVE tools to look up real-time info. "
                       "If you don't know something, or need the current time/weather, USE A TOOL."),
            ("human", "{input}"),
            # This placeholder is where the agent "thinks"
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        external_tools = load_tools(["wikipedia", "serpapi"], llm=llm)  
        tools = external_tools + [get_weather]

        # FIX 2: Use create_tool_calling_agent (Best for Groq/Llama 3.3)
        # Use keyword arguments for everything to avoid syntax errors
        agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

        # FIX 3: You need an AgentExecutor to actually run the loop
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        print("--- Calling the Agent ---")
        response = agent_executor.invoke({"input": question})
        
        return {
            "yourQuistion": question, 
            "response": response["output"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))