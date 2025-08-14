from app.state.appointment_state import graph_builder
from app.nodes.user_info import extract_user_info
from app.nodes.check_user_info import check_missing_info
from app.nodes.ask_to_confirm import ask_to_confirm
from app.nodes.suggest_slots import suggest_slots
from app.nodes.classify_the_intent import classify_the_intent
from app.nodes.inquire_required_info import inquire_required_info
from app.nodes.chitchat_or_joke import chitchat_or_joke
from app.nodes.execute_booking import execute_booking
from app.nodes.cancel_booking import cancel_booking
from langgraph.graph import START, END
from app.config import checkpointer  # ✅ Import shared instance

graph_builder.add_node('classify_the_intent', classify_the_intent)
graph_builder.add_node('extract_input', extract_user_info)
graph_builder.add_node('check_missing_input', check_missing_info)
graph_builder.add_node('ask_to_confirm', ask_to_confirm)
graph_builder.add_node('execute_booking', execute_booking)
graph_builder.add_node('cancel_booking', cancel_booking)
graph_builder.add_node('inquire_required_info', inquire_required_info)
graph_builder.add_node("suggest_slots", suggest_slots)
graph_builder.add_node("chitchat_or_joke", chitchat_or_joke)

graph_builder.add_conditional_edges(
    "classify_the_intent",
    lambda state: state.get("next_node", END)
)
graph_builder.add_conditional_edges(
    "check_missing_input",
    lambda state: state.get("next_node", END)
)
graph_builder.add_conditional_edges(
    "ask_to_confirm",
    lambda state: state.get("next_node", END)
)

graph_builder.add_edge(START, 'classify_the_intent')
graph_builder.add_edge('extract_input', 'check_missing_input')
graph_builder.add_edge('execute_booking', END)
graph_builder.add_edge('cancel_booking', END)

# ✅ Compile with the shared checkpointer
graph_app = graph_builder.compile(checkpointer=checkpointer)
