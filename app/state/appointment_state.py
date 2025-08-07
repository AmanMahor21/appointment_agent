from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    patient_name: str
    user_id: str
    appointment_date: str
    appointment_time: str
    last_prompted_for: str
    next_node: str
    confirmation_response: str
    # waiting_for: str
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)
