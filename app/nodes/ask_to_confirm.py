

from app.prompt import ASK_CONFIRM_PROMPT, CLASSIFY_CONFIRM_PROMPT
from app.state.appointment_state import State
from app.llm import appointment_agent
from langgraph.types import interrupt
from app.helpers import send_msg_to_telegram


async def ask_to_confirm(state: State) -> State:
    llm = appointment_agent()

    # print(state, 'askkk')

    if not state.get("confirmation_response"):
        info_str = "\n".join(f"{k}: {v}" for k, v in {
            "patient_name": state["patient_name"],
            "appointment_date": state["appointment_date"],
            "appointment_time": state["appointment_time"],
        }.items())
        print(state, 'askkk')

        extracted = (ASK_CONFIRM_PROMPT | llm).invoke({"info": info_str})

        if state.get("user_id"):
            await send_msg_to_telegram(
                state["user_id"],
                body=extracted.content.split("</think>")[-1]
            )

        return interrupt(state)

    user_reply = state.get('confirmation_response')
    # print(user_reply, 'replayy')
    raw_intent = (CLASSIFY_CONFIRM_PROMPT | llm).invoke(
        {"reply": user_reply}).content.strip().lower()
    intent = raw_intent.split("</think>")[-1].strip().lower()
    if intent.lower() == "yes":
        print(intent, 'underr')
        state["next_node"] = "execute_booking"
        print("Before return YES branch:", state)
        return state
    else:
        print("Before return YES branch:", state, 'nott')
        state["next_node"] = "cancel_booking"
        return state
