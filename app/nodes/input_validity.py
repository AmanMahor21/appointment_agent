
from app.llm import appointment_agent
from app.state.appointment_state import State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.helpers import send_msg_to_telegram
from datetime import datetime, timedelta

# Add this inside your function before or after time validation


def is_weekend(date_str: str) -> bool:
    """Check if the given date is on a weekend. Expects 'YYYY-MM-DD' format."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.weekday() >= 5  # 5 = Saturday, 6 = Sunday
    except ValueError:
        return False  # Handle invalid format gracefully


def get_next_weekday(date_str: str) -> str:
    """If the date is a weekend, shift to the next Monday."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    while date_obj.weekday() >= 5:  # While it's Saturday or Sunday
        date_obj += timedelta(days=1)
    return date_obj.strftime('%Y-%m-%d')


async def input_validity(state: State) -> State:
    extract_prompt = ChatPromptTemplate.from_messages([
        ("system", """Validates if the given time (like '9:00 AM' or '4:30 PM') falls within clinic hours (10:00 AM to 1:00 PM) and (2:00 PM to 5:00 PM). Returns 'valid' or 'invalid'."""),
        ("user", "{user_message}")
    ])

    appointment_time = state['appointment_time']
    # You must ensure this key is set earlier
    appointment_date = state.get('appointment_date')

    # Check if appointment date falls on a weekend
    if is_weekend(appointment_date):
        suggested_date = get_next_weekday(appointment_date)
        state['appointment_date'] = suggested_date
        if state["user_id"]:
            await send_msg_to_telegram(
                state["user_id"],
                body=f"⚠️ The selected date ({appointment_date}) falls on a weekend. We've adjusted it to the next available weekday: {suggested_date}."
            )

    # Continue time validation as you already do
    llm = appointment_agent()
    try:
        chain = extract_prompt | llm
        extracted = chain.invoke({"user_message": appointment_time})
        if state["user_id"]:
            res = await send_msg_to_telegram(
                state["user_id"],
                body=extracted.content.split("</think>")[-1])
        if res == 200:
            return state
    except Exception as e:
        print("❌ Failed to parse LLM response")
        raise e

    return state
