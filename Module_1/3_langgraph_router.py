from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END, add_messages
from langgraph.prebuilt import  ToolNode, tools_condition
from typing import TypedDict, Annotated, List
from langchain_core.messages import AnyMessage 
import pprint

model = ChatOpenAI(model="gpt-4o-mini")

# Functions
def multiply(a: int, b: int):
    """
    This function return the product of two integers
    """
    return a*b

def add(a: int, b: int):
    """
    This function return the Addition of two integers
    """
    return a+b

# Binding tools with model
tools= [add, multiply]
llm_tool_calling = model.bind_tools(tools)

# State
class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


# Nodes
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_tool_calling.invoke(state["messages"])]}

# Build Graph
builder = StateGraph(State)

#Add Nodes
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([add, multiply])) #Add another node that helps with tool calling

#Add Edges
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm",
                              # The tool condition routes the edges based on the output of AIMessage
                              # If AIMessage provoke toolcalling, according tool will be called.
                              # Else it just End with AIMessage
                              tools_condition)
builder.add_edge("tools", END)
graph = builder.compile()

query = {"messages": "3*3"}
reponse = graph.invoke(query)
data = reponse['messages'][-1].content
    