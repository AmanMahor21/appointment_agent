from langgraph.graph import StateGraph
from app.state.appointment_state import State
from app.helpers import get_available_slots
from langchain_core.prompts import PromptTemplate
from app.llm import appointment_agent
from app.helpers import send_msg_to_telegram


extract_prompt = PromptTemplate.from_template("""
You are a helpful assistant helping patients book appointments.

Present the suggested time slots {slot} in a clear and natural way.
Do not list them in a single sentence. Use line breaks to separate each slot.
Make sure the message sounds warm and patient-friendly.
Do not over explain.
""")


async def suggest_slots(state: State):
    """Node for explicit slot suggestion flow"""

    slots = get_available_slots(
        date=state.get("appointment_date")
    )
    llm = appointment_agent()
    formatted_prompt = extract_prompt.invoke({"slot": slots})
    llm_res = llm.invoke(formatted_prompt)
    # print(llm_res, 'suggesttt')

    res_for_user = llm_res.content.split("</think>")[-1]
    missing_fields = []
    if len(res_for_user) > 1:
        res = await send_msg_to_telegram(
            state["user_id"], body=res_for_user)
        if res == 200:
            state["last_prompted_for"] = missing_fields

    state["available_slots"] = slots  # Store for confirmation
    return state

# Add to your graph
