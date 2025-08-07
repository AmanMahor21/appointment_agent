
from app.prompt import CANCEL_BOOKING_PROMPT
from app.state.appointment_state import State
from app.llm import appointment_agent
# from langgraph.types import asd
from app.config import checkpointer
from app.helpers import insert_booking
from app.helpers import send_msg_to_telegram
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
            await checkpointer.delete_thread(state.get("user_id"))
            # return {
            #     "user_id": state["user_id"],
            #     "messages": [],
            #     "next_node": "",
            #     "patient_name": "",
            #     "appointment_time": "",
            #     "appointment_date": "",
            #     "last_prompted_for": ""
            # }
