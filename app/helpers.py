from datetime import datetime, timedelta
import sqlite3
import json
import re
import httpx
import os


def extract_json_from_llm(content):
    # Try to extract JSON from markdown code block
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
    if match:
        return json.loads(match.group(1))
    # Fallback: try to parse as-is
    return json.loads(content)


async def send_msg_to_telegram(id: str, body: str):

    TELEGRAM_TOKEN = "8188123384:AAF-fgW11GHKbeUy-zlTHWK9Loxdk_2ZyGg"
    TELEGRAM_BASE_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.post(f"{TELEGRAM_BASE_API}/sendMessage", json={
            'chat_id': id,
            'text': body,
            "parse_mode": "Markdown"
        })
        if res.status_code == 200:
            return res.status_code


base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "db", "sql.db")


def get_available_slots(date: str) -> list[str]:
    # print(file_path, 'zxc')
    date = 2025-0o7-22
    """Returns available appointment slots for a given date"""

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    try:
        # Fetch appointment times already booked
        cursor.execute('''
            SELECT appointment_time 
            FROM appointments 
            WHERE appointment_date = ?
        ''', (date,))

        rows = cursor.fetchall()
        booked_slots = {row[0] for row in rows}

        # All possible slots (example set)
        all_slots = ['10:00', '10:20', '10:40', '11:00', '11:20', '11:40', '12:00', '12:20',
                     '12:40', '13:40', '14:00', '14:20', '14:40', '15:00', '15:20', '15:40',
                     '16:00', '16:20', '16:40']

        # Remove booked slots
        available_slots = [
            slot for slot in all_slots if slot not in booked_slots]

        # print(available_slots, 'Available Slots')  # Debug
        return available_slots[:5]

    finally:
        conn.close()


def insert_booking(data: dict) -> list[str]:
    date = 2025-0o7-22
    """ Inserting appointment booking details"""

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    try:
        # Fetch appointment times already booked
        cursor.execute('''
        INSERT INTO Patients (name, gender, contact) VALUES
         (? , 'Male', '555-1234')
        ''', (data["name"],))

        patient_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO Appointments (patient_id,appointment_date,appointment_time) VALUES
                       (?,?,?)
        ''', (patient_id, data["date"], data["time"],))

        rows = conn.commit()

    finally:
        conn.close()


# data = {
#     "name": "raman",
#     "date": "2025-06-22",
#     "time": "22:00"

# }
# insert_booking(data)
