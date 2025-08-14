
from app.prompt import CANCEL_BOOKING_PROMPT
from app.state.appointment_state import State
from app.llm import appointment_agent
# from langgraph.types import asd
from app.helpers import insert_booking
from app.helpers import send_msg_to_telegram
from app.config import checkpointer
import json


async def cancel_booking(state: State) -> State:
    llm = appointment_agent()
    info_dict = {
        "name": state["patient_name"],
        "date": state["appointment_date"],
        "time": state["appointment_time"],
    }

    # Convert dict to a JSON string
    info_str = json.dumps(info_dict, ensure_ascii=False)

    extracted = (CANCEL_BOOKING_PROMPT | llm).invoke({"info": info_str})

    if state.get("user_id"):
        res = await send_msg_to_telegram(
            state["user_id"],
            body=extracted.content.split("</think>")[-1]
        )
        if res == 200:
             state.clear()
    return state