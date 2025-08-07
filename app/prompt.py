# prompts.py
from langchain_core.prompts import PromptTemplate

ASK_CONFIRM_PROMPT = PromptTemplate.from_template(
    "You are a healthcare assistant.\n"
    "Please show the following collected info to the user for confirmation:\n"
    "{info}\n\n"
    "Ask the user: 'Do you confirm these details? in natural language'\n"
    "Reply with only 'Yes' or 'No'.")

CLASSIFY_CONFIRM_PROMPT = PromptTemplate.from_template(
    "Classify the following reply as exactly 'yes' or 'no',:\n"
    "Reply: {reply}\n"
    "Return only the label."
)


BOOKING_SUCCESS_PROMPT = PromptTemplate.from_template(
    "You are a healthcare assistant.\n"
    "The patient's appointment has been successfully booked with the following details:\n"
    "{info}\n"
    "Write a warm and friendly confirmation message for the user in natural language.\n"
    "Keep it short and clear.\n"
)

CANCEL_BOOKING_PROMPT = PromptTemplate.from_template(
    "Given the following appointment information:/n"
    "{info}/n"
    " Respond with a short, natural sentence confirming the appointment has been cancelled./n"
    "Example: Your appointment with Dr. Smith on 5th August at 3:00 PM has been cancelled."
    "Do not include any additional text, instructions, or explanations."
)

# "Example: 'Great news! Your appointment with Dr. Smith is confirmed for 22 June 2025 at 10:00 AM.'"
