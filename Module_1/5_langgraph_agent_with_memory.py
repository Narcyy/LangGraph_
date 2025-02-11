from langchain_openai import ChatOpenAI
from langgraph.graph import START,END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
import pprint
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY") 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
llm = ChatOpenAI(model='gpt-4o-mini')

# Functions 
def add(a: int, b: int):
    """
    This function returns the addition of two integers.
    """
    return a+b

def multiply(a: int, b: int):
    """
    This function returns the multiplication of two integers.
    """
    return a*b

def divide(a: int, b: int):
    """
    This function returns the division of two integers.
    """
    return a//b

# Binding tools with llm model
tools = [add, multiply, divide]
llm_with_tools = llm.bind_tools(tools)

# State
class State(MessagesState):
    pass

# Node
def tool_calling_llm(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build Graph
builder = StateGraph(State)

builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", "tool_calling_llm")

# Creating checkpoint
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Specify a thread
config = {"configurable":{"thread_id":"123"}}

query = {"messages":"What 3*3?"}

response = graph.invoke(query, config)

data = response['messages'][-1].content
print(data)
