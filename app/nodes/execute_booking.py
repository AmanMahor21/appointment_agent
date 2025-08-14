from app.prompt import BOOKING_SUCCESS_PROMPT
from app.state.appointment_state import State
from app.llm import appointment_agent
from app.config import checkpointer  # ✅ Same shared instance
from app.helpers import insert_booking
from app.helpers import send_msg_to_telegram
import json

async def execute_booking(state: State) -> State:
    llm = appointment_agent()
    info_dict = {
        "name": state["patient_name"],
        "date": state["appointment_date"],
        "time": state["appointment_time"],
    }

    # Save booking
    insert_booking(info_dict)
    info_str = json.dumps(info_dict, ensure_ascii=False)

    # Generate booking confirmation text
    extracted = (BOOKING_SUCCESS_PROMPT | llm).invoke({"info": info_str})

    if state.get("user_id"):
        res = await send_msg_to_telegram(
            state["user_id"],
            body=extracted.content.split("</think>")[-1]
        )
        if res == 200:
            state.clear()
    return state
