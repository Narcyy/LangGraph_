from langgraph.graph import START, END, StateGraph, MessagesState
from langchain_openai import ChatOpenAI
import asyncio

llm = ChatOpenAI(model = "gpt-4o-mini")

async def bot(state: MessagesState):
    response = await llm.ainvoke(state["messages"])
    return {"messages":response}

builder = StateGraph(MessagesState)

builder.add_node("bot", bot)

builder.add_edge(START, "bot")
builder.add_edge("bot",END)

graph = builder.compile()

async def get_response(user_input: str):
    result = await graph.ainvoke(user_input)
    return {"messages": result}
user_input = {"messages":"What is 4*4: "}
result = asyncio.run(get_response(user_input))
print(result['messages']['messages'][-1].content)
