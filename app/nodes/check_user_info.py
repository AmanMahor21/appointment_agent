import httpx
from fastapi import APIRouter, Request
from app.helpers import send_msg_to_telegram
from app.llm import appointment_agent
from app.state.appointment_state import State
from langchain_core.prompts import PromptTemplate
from langgraph.graph import END

TELEGRAM_TOKEN = "8188123384:AAF-fgW11GHKbeUy-zlTHWK9Loxdk_2ZyGg"
TELEGRAM_BASE_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

extract_prompt = PromptTemplate.from_template("""
You are a helpful assistant helping patients book appointments.

So far, you have collected the following:
- Patient name: {patient_name}
- Appointment date: {appointment_date}

Please ask the user for whatever is missing, in a polite and natural sentence.
""")


async def check_missing_info(state: State) -> State | str:
    llm = appointment_agent()
    last_msg = state['messages'][-1].content
    # print(state, 'user infooooo')

    state_fields = ["patient_name", "appointment_date"]

    missing_fields = [x for x in state_fields if not state.get(x)]

    if state["appointment_time"]:
        state["next_node"] = "ask_to_confirm"
        return state

    if not missing_fields:
        # ✅ All fields are filled — skip follow-up
        print("All info collected. No follow-up needed.")
        state["last_prompted_for"] = []
        state["next_node"] = "suggest_slots"  # 👈 store this as a flag
        # state["next_node"] = "ask_to_confirm"  # 👈 store this as a flag
        return state

    if set(state.get("last_prompted_for", [])) == set(missing_fields):
        return state
    # extracted = extract_prompt.invoke({"input": last_msg})

    prompt_text = extract_prompt.invoke({
        "patient_name": state.get("patient_name", ""),
        "appointment_date": state.get("appointment_date", ""),
        # "appointment_time": state.get("appointment_time", ""),
        # "doctor_name": state.get("doctor_name", ""),
    })

    follow_up_message = llm.invoke(prompt_text)

    # 📬 Send via Telegram
    user_id = state.get("user_id")
    if user_id:
        res = await send_msg_to_telegram(
            state["user_id"], body=follow_up_message.content.split(
                "</think>")[-1])
        if res == 200:
            state["last_prompted_for"] = missing_fields
            state["next_node"] = END

    return state


# import httpx
# from fastapi import APIRouter, Request
# from app.helpers import send_msg_to_telegram
# from app.llm import appointment_agent
# from app.state.appointment_state import State
# from langchain_core.prompts import PromptTemplate
# TELEGRAM_TOKEN = "8188123384:AAF-fgW11GHKbeUy-zlTHWK9Loxdk_2ZyGg"
# TELEGRAM_BASE_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# extract_prompt = PromptTemplate.from_template("""
# You are a helpful assistant helping patients book appointments.

# So far, you have collected the following:
# - Patient name: {patient_name}
# - Appointment date: {appointment_date}
# - Appointment time: {appointment_time}

# Please ask the user for whatever is missing, in a polite and natural sentence.
# """)


# async def check_missing_info(state: State) -> State | str:
#     llm = appointment_agent()
#     last_msg = state['messages'][-1].content
#     print(state, 'user infooooo')

#     state_fields = ["patient_name", "appointment_date", "appointment_time"]

#     missing_fields = [x for x in state_fields if not state.get(x)]

#     print(state, 'qqqqqqqw')

#     if not missing_fields:
#         # ✅ All fields are filled — skip follow-up
#         print("All info collected. No follow-up needed.", state)
#         state["last_prompted_for"] = []
#         state["next_node"] = "suggest_slots"  # 👈 store this as a flag
#         # state["next_node"] = "ask_to_confirm"  # 👈 store this as a flag
#         return state

#     if state.get("last_prompted_for") == missing_fields:
#         return state
#     # extracted = extract_prompt.invoke({"input": last_msg})

#     prompt_text = extract_prompt.invoke({
#         "patient_name": state.get("patient_name", ""),
#         "appointment_date": state.get("appointment_date", ""),
#         "appointment_time": state.get("appointment_time", ""),
#         # "doctor_name": state.get("doctor_name", ""),
#     })

#     follow_up_message = llm.invoke(prompt_text)
#     print(follow_up_message.content.split(
#         "</think>")[-1], '👉 Follow-up to send to user')

#     # 📬 Send via Telegram
#     user_id = state.get("user_id")
#     if user_id:
#         res = await send_msg_to_telegram(
#             state["user_id"], body=follow_up_message.content.split(
#                 "</think>")[-1])
#         if res == 200:
#             state["last_prompted_for"] = missing_fields

#     return state
