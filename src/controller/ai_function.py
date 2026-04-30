from langchain_classic.agents import AgentExecutor,create_tool_calling_agent
from fastapi import HTTPException
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import DuckDuckGoSearchRun  
from src.tools import get_weather,gettime


def ask_question(question: str):
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            timeout=30
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use tools to look up real-time information like current things current age current time or other live dettails if use need current news without this type of quistion dont use tools just user normal lmm to give them ans when necessary."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        search_tool = DuckDuckGoSearchRun()
        tools = [search_tool, get_weather, gettime]

        agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True
        )

        response = agent_executor.invoke({"input": question})
        print(f"response is this from log{str(response)}")
        return {
            "yourQuistion": question,
            "response": response["output"]
        }
    except Exception as e:
        print(f"error is this {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))