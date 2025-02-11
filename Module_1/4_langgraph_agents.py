from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY") 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"

llm = ChatOpenAI(model = "gpt-4o-mini")

# Functions
def mutliply(a: int, b: int):
    """
    Returns multiplication of given two integers.
    """
    return a*b

def add(a: int, b: int):
    """
    Returns Addition of given two integers.
    """
    return a+b

def substract(a: int, b: int):
    """
    Returns division of given two integers.
    """
    return a - b

# Bind the tools with model
tools = [mutliply, add, substract]
llm_with_tools = llm.bind_tools(tools)

# State
class State(MessagesState):
    pass

# sys_text = [("system","You are an helpfull AI assistant that helps with mathematical operations.")]

# Node
def llm_calling_node(state: State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

# Build Graph
builder = StateGraph(State)

# Adding Nodes
builder.add_node("llm_calling_node", llm_calling_node)
builder.add_node("tools", ToolNode(tools))

# Adding Edges
builder.add_edge(START, "llm_calling_node")
builder.add_conditional_edges("llm_calling_node", tools_condition)
builder.add_edge("tools", "llm_calling_node")

graph = builder.compile()

query = {"messages":"mutiply 4 with 5, add 5 to it, and finally substract entire output with 5"}
response = graph.invoke(query)

data = response['messages'][-1].content
print(data)
