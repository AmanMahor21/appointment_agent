from app.helpers import send_msg_to_telegram
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.state.appointment_state import State
from app.llm import appointment_agent


# Define the JSON output schema

async def inquire_required_info(state: State) -> State:
    last_msg = state['messages'][-1].content

    extract_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a friendly and professional assistant that helps users book, update, or cancel doctor appointments.

Your task is:
1. Understand whether the user wants to **book**, **cancel**, or **reschedule** an appointment.
2. Respond with only the information required for that specific action.
3. Be brief, polite, and clear.

Rules:
- For **booking**, ask for: full name preferred date
- For **canceling**, ask for: full name and original appointment details (like doctor or time).
- For **rescheduling**, ask for: full name and new date for booking.

Examples:

User: "What info do I need to book an appointment?"
→ Assistant: "To book an appointment, I’ll need your full name, preferred doctor or department, date and time, and a contact number."

User: "How do I cancel my appointment?"
→ Assistant: "To cancel an appointment, just provide your full name and details like the doctor or date. I’ll take care of the rest."

User: "What do you need to reschedule?"
→ Assistant: "To reschedule, I just need your name and the new date or time you'd prefer. I’ll handle the update."

Now based on the user's message below, give a polite, specific response asking for only the needed info:
"""),
        ("user", "{user_message}")
    ])

    try:
        llm = appointment_agent()
        chain = extract_prompt | llm
        extracted = chain.invoke({"user_message": last_msg})
        response = extracted.content.split("</think>")[-1].strip()

        if state["user_id"]:
            res = await send_msg_to_telegram(state["user_id"], body=response)
            if res == 200:
                return state

    except Exception as e:
        print("❌ Failed to handle ask_info_requirements")
        raise e

    return state
