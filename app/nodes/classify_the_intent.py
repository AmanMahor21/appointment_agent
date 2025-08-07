
from app.llm import appointment_agent
from app.state.appointment_state import State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.helpers import send_msg_to_telegram


# Define the JSON output schema

async def classify_the_intent(state: State) -> State:

    extract_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant for booking doctor appointments.

Classify the user's message into one of the following intent categories.  
**Each intent is listed with a description for your understanding.**  
**Your response must be ONLY the intent name (no description, no extra text).**

1. inquire_required_info – The user expresses the desire to book, cancel, or reschedule an appointment, or asks how to do so.
2. ask_booking_details - if the user is asking about their current booking info.
3. extract_input - if the user is providing appointment details like name, date, doctor, or time.
4. clarification_needed — user asks about purpose of a question (e.g. 'why do you need my phone number?')
5. hesitation_or_delay — user is unsure or stalling (e.g., 'let me think')
6. chitchat_or_joke – the user says something casual or unrelated (e.g., greetings, jokes, thanks, sarcasm, vague help requests like "Can you help me?")
         
**Instructions:**
- Reply with ONLY the intent name (e.g., ask_booking_details).
- Do NOT include any description, explanation, or extra text.
             
**Examples:**
BAD: inquire_required_info – The user wants to reschedule.
BAD: The intent is inquire_required_info.
GOOD: inquire_required_info
         
         Respond with only the intent name (e.g., ask_info_requirements)."""),
        ("user", "{user_message}")
    ])

    # Get the last user message
    last_msg = state['messages'][-1].content
    # Debug: Print the generated prompt

    # Get LLM
    llm = appointment_agent()

    # Invoke the chain
    try:
        chain = extract_prompt | llm
        extracted = chain.invoke({"user_message": last_msg})

        state["next_node"] = extracted.content.split("</think>")[-1].strip()

        # if state["user_id"]:
        #     res = await send_msg_to_telegram(
        #         state["user_id"], body=extracted.content.split(
        #             "</think>")[-1])
        # if res == 200:
        #     return state
        # print("Parsed Output: ask user", extracted)
    except Exception as e:
        print("❌ Failed to parse LLM response")
        raise e

    # Return updated state
    return state

# 8. unknown — can't classify
