from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
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
    messages: List[Union[HumanMessage, AIMessage]]

# 初始化 LLM，传入公司的 API endpoint
llm = ChatOpenAI(
    model=model_name,
    openai_api_base=api_base,
    openai_api_key=api_key,
    temperature=0.0
)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"]) 

    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []

user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    #sent the input to the graph to use llm to operate
    result = agent.invoke({"messages": conversation_history})
    #save the conversation history
    conversation_history = result["messages"]
    user_input = input("Enter: ")

with open("logging.txt", "w", encoding="utf-8") as file:
    file.write("Your Conversation Log:\n")

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")