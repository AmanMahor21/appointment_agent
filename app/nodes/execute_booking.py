
from app.prompt import BOOKING_SUCCESS_PROMPT
from app.state.appointment_state import State
from app.llm import appointment_agent
from app.agent.appointment_agent import checkpointer
# from langgraph.types import asd
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

    # Convert dict to a JSON string
    insert_booking(info_dict)
    info_str = json.dumps(info_dict, ensure_ascii=False)

    extracted = (BOOKING_SUCCESS_PROMPT | llm).invoke({"info": info_str})

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
