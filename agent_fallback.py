# agent_fallback.py 

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from main import rag_chain

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

search_tool = DuckDuckGoSearchRun()

prompt = ChatPromptTemplate.from_messages([
    ("system", "तुम एक भक्तिपूर्ण AI हो। अगर जवाब गीता/रामचरितमानस में नहीं मिले तो Google से सर्च करो।"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, [search_tool], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=False)

def agent_answer(question, chat_history=[]):
    try:
        rag_result = rag_chain(question)
        if len(rag_result) < 60 or "नहीं मिला" in rag_result:
            # chat_history
            formatted_history = []
            for m in chat_history:
                if m["role"] == "user":
                    formatted_history.append(HumanMessage(content=m["content"]))
                else:
                    formatted_history.append(AIMessage(content=m["content"]))
            
            response = agent_executor.invoke({
                "input": question,
                "chat_history": formatted_history
            })
            return response["output"]
        return rag_result
    except:
        formatted_history = []
        for m in chat_history:
            if m["role"] == "user":
                formatted_history.append(HumanMessage(content=m["content"]))
            else:
                formatted_history.append(AIMessage(content=m["content"]))
        
        response = agent_executor.invoke({
            "input": question,
            "chat_history": formatted_history
        })

        return response["output"]
