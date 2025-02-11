from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
# Creating funtion
def multiply(a, b):
    """
    This function return the product of two integers.
    """
    return a*b

#Binding the tools with model
tools = [multiply]
llm_tool_calls = model.bind_tools(tools)

#State
class MessagesState(MessagesState):
    pass
# Node
def tool_calling_llm(state: MessagesState):
    print([llm_tool_calls.invoke(state["messages"])])
    return {"messages": [llm_tool_calls.invoke(state["messages"])]}

# Build Graph
builder = StateGraph(MessagesState)

# Adding Nodes
builder.add_node("tool_calling_llm", tool_calling_llm)

# Adding Edges
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)

graph = builder.compile()
query = {"messages": "Mutiply 3 with 3"}
response = graph.invoke(query)

