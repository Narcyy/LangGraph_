from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import random
from langchain.schema.output_parser import StrOutputParser
#State
class State(TypedDict):
    graph_state: str

# Nodes
def node_1(state):
    print("---Node 1---")
    return {"graph_state":state['graph_state']}

def node_2(state):
    print("---Node 2---")
    return {"graph_state":state['graph_state']+ "I am Happy"}

def node_3(state):
    print("---Node 3---")
    return {"graph_state":state['graph_state']+ "I am Sad"}

# Build Graph
builder =StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)


def decide_mood(state):
     if random.random() < 0.5:
         return "node_2"
     return "node_3"

#Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

#ADD
graph = builder.compile()


#Invokation
response = graph.invoke({"graph_state": "Hello I am Narcy, "})

print(response["graph_state"])

