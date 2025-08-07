
from dotenv import load_dotenv
from app.db.sqlite import sql_engine
from langgraph.prebuilt import create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
import json
import requests
from openai import OpenAI
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import os
load_dotenv()
# from app.prompt import agent_prompt, sql_prompt
# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    # Replace with your actual key
    api_key=os.getenv("OPENROUTER_API")
)

# try:
# llm = ChatOpenAI(
#     model="deepseek/deepseek-chat-v3-0324:free",
#     temperature=0,
#     openai_api_key=client.api_key,
#     openai_api_base=str(client.base_url),
#     max_retries=1
# )

llm = ChatGroq(
    api_key=os.getenv("GROK_API_KEY"),
    model_name="deepseek-r1-distill-llama-70b",
    temperature=0.1
)

# except:


def appointment_agent():

    return llm
