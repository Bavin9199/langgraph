from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os

# 设置代理（如果需要出公司内网）
os.environ["HTTP_PROXY"] = "http://10.144.1.10:8080"
os.environ["HTTPS_PROXY"] = "http://10.144.1.10:8080"

# 读取 .env 文件
load_dotenv()

# 从环境变量里拿配置
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
model_name = os.getenv("MODEL_NAME", "google/gemma-3-12b-it")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int):
    """this is an addition function that add two numbers together"""

    return a + b

@tool
def subtract(a: int,b: int):
    """this is a substraction function"""
    return a - b

@tool 
def multiply(a: int,b: int):
    """this is a multiply function"""
    return a * b

tools = [add, subtract, multiply]

model = ChatOpenAI(model=model_name).bind_tools(tools)


def model_call(state:AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best of your ability."
    )
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages":[("user", "40 divided by 6.")]}
print_stream(app.stream(inputs,stream_mode="values"))