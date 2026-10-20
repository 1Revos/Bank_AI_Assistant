from typing_extensions import TypedDict, Literal, Optional
from langgraph.graph import StateGraph, START, END, MessagesState
from IPython.display import Image, display

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from promts import sys_messg1, sys_messg2

load_dotenv()

sys_messg_topic = SystemMessage(content = sys_messg1)
sys_messg_global = SystemMessage(content = sys_messg2)

llm = ChatOpenAI(model = "gpt-6-luna")

class State(MessagesState):
    result: Optional[str]
    topic: Optional[str]
    total_calls: int

#Nods

def assistent(state: State) -> dict:
    return {"messages": llm.invoke([sys_messg_topic] + state["messages"]), "result": state["result"], "topic": state["topic"], "total_calls": state["total_calls"] + 1}

def assistent1(state: State) -> dict:
    return {"messages": llm.invoke([sys_messg_global] + state["messages"]), "result": state["result"], "topic": state["topic"], "total_calls": state["total_calls"] + 1}

#Change

def node_change(state: State) -> Literal["node_1", "node_2"]:

    total_calls = state["total_calls"]
    topic = state["topic"]

    if total_calls < 2 and topic is None:
        return "node_1"
    else:
        return "node_2"

#Tools


