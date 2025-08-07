
from app.llm import appointment_agent
from app.state.appointment_state import State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

today_str = datetime.now().date().isoformat()

# Define the JSON output schema


class Person(BaseModel):
    """Information about appointment."""
    patient_name: Optional[str] = Field(None, description="The patient_name")
    appointment_date: Optional[str] = Field(
        None, description="The appointment_date")
    appointment_time: Optional[str] = Field(
        None, description="The appointment_time")


def extract_user_info(state: State) -> State:
    parser = PydanticOutputParser(pydantic_object=Person)

    extract_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""You are an assistant that extracts structured information from user input.

Extract the following fields from the user's message:
- patient_name
- appointment_date
- appointment_time
- user_id

📅 Date Instructions:
- Always convert relative or fuzzy phrases like "tomorrow", "next day", "tues", or misspellings like "tmrw", "tomorow" into an ISO 8601 date format (YYYY-MM-DD).
- Assume "today" is {today_str}.
- If the date is not provided, leave the field as null.

Respond ONLY in the following JSON format:
{{format_instructions}}"""
        ),
        ("human", "{input}")
    ]).partial(format_instructions=parser.get_format_instructions())

    # Get the last user message
    last_msg = state['messages'][-1].content
    # print(state, 'pooo')
    # Debug: Print the generated prompt

    # Get LLM
    llm = appointment_agent()

    # Invoke the chain
    try:
        chain = extract_prompt | llm | parser
        extracted = chain.invoke({"input": last_msg})
    except Exception as e:
        print("❌ Failed to parse LLM response")
        raise e

    # Return updated state
    return {
        **state,
        "patient_name": state.get("patient_name") or extracted.patient_name,
        "appointment_date": state.get("appointment_date") or extracted.appointment_date,
        "appointment_time": state.get("appointment_time") or extracted.appointment_time,
        # "doctor_name": state.get("doctor_name") or extracted.doctor_name,
    }
