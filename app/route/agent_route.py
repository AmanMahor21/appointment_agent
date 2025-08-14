from fastapi import APIRouter, Request
from langchain_core.messages import HumanMessage
from app.llm import appointment_agent
from app.agent.appointment_agent import graph_app
from app.helpers import send_msg_to_telegram
from app.state.appointment_state import State

# import httpx
import os
from langchain_core.prompts import ChatPromptTemplate

from langgraph.types import Command

router = APIRouter()

TELEGRAM_TOKEN = "8188123384:AAF-fgW11GHKbeUy-zlTHWK9Loxdk_2ZyGg"
TELEGRAM_BASE_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

grok_key = os.getenv('GROK_API_KEY')

extract_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract patient_name, appointment_date, appointment_time, doctor_name, user_id from this message. Reply in JSON."),
    ("human", "{input}")
])


@router.post("/webhook/telegram")
async def telegram_webhook(req: Request):
    data = await req.json()
    chat_id = data["message"]["chat"]['id']
    question = data['message']['text']


    messages = [HumanMessage(content=question)]
    config = {"configurable": {"thread_id": str(chat_id)}}

    state = await graph_app.aget_state(config)
    if state.interrupts:

        await graph_app.aupdate_state(
            config,
            {**state.values, "confirmation_response": question}
        )
        response = await graph_app.ainvoke(Command(resume={}),config=config)
    else:
        response = await graph_app.ainvoke({"messages": messages, "user_id": str(chat_id)}, config=config)
        # print(response, 'zzzcc')

    if "__interrupt__" in response:
        interrupt_value = response["__interrupt__"][0].value
        return {"status": "waiting"}

    # Otherwise, send bot's latest response
    # if "messages" in response and response["messages"]:
    #     await send_msg_to_telegram(chat_id, response["messages"][-1].content)

    # return {"status": "ok"}
