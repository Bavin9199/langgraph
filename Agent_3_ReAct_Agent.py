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

