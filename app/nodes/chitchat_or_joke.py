from app.helpers import send_msg_to_telegram
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.state.appointment_state import State
from app.llm import appointment_agent


# Define the JSON output schema

async def chitchat_or_joke(state: State) -> State:
    # Get the last user message
    last_msg = state['messages'][-1].content

    # Set up prompt
    extract_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a friendly, polite assistant that helps users book doctor appointments.

Sometimes users send casual or unrelated messages — like greetings, thank-yous, jokes, vague help requests, or sarcastic remarks.

No matter what they say, respond naturally and respectfully. Acknowledge their message warmly, and gently guide them back to the purpose: booking or managing a doctor’s appointment.

Examples:
User: "Hi there!"
→ Assistant: "Hello! 👋 I can help you book, update, or cancel a doctor appointment. What would you like to do?"

User: "Can you do magic too? 😄"
→ Assistant: "Haha, I wish! But I’m here to help you with doctor appointments. Would you like to book or change one?"

User: "Can you help me? I’m kinda confused."
→ Assistant: "Of course! I’m here to help with booking or managing doctor appointments. What would you like to do?"

Now respond naturally to the user's message below.

Respond in a friendly, short paragraph — no JSON, no labels."""),
        ("user", "{user_message}")
    ])

    try:
        llm = appointment_agent()
        chain = extract_prompt | llm
        extracted = chain.invoke({"user_message": last_msg})
        response = extracted.content.split("</think>")[-1].strip()

        # state["next_node"] = response

        if state["user_id"]:
            res = await send_msg_to_telegram(state["user_id"], body=response)
            if res == 200:
                return state

    except Exception as e:
        print("❌ Failed to handle chitchat or joke")
        raise e
    return state
