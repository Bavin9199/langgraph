from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
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

print("API KEY:", api_key)
print("API BASE:", api_base)
print("MODEL:", model_name)

# 定义 Agent 的状态
class AgentState(TypedDict):
    messages: List[HumanMessage]

# 初始化 LLM，传入公司的 API endpoint
llm = ChatOpenAI(
    model=model_name,
    openai_api_base=api_base,
    openai_api_key=api_key,
    temperature=0.0
)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")