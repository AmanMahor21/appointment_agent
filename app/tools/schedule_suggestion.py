import sqlite3
from datetime import datetime, timedelta


def get_available_slots(date):
    """Returns available slots with buffer time consideration"""
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    try:
        booked_slots = cursor.execute('''
        SELECT appointment_time 
        FROM appointments 
        WHERE appointment_date = ?
         ''', (date))

        # Generate all possible slots (e.g., 9 AM - 5 PM, every 15 mins)
        all_slots = ['10:00', '10:20', '10:40', '11:00', '11:20', '11:40', '12:00', '12:20',
                     '12:40', '13:40', '14:00', '14:20', '14:40', '15:00', '15:20', '15:40', '16:00', '16:20', '16:40']

    # Filter out booked slots + apply buffer rules
        # available = [slot for slot in all_slots if slot not in booked_slots]

        availabe_slot = [
            slot for slot in all_slots if slot not in booked_slots]

        return availabe_slot[:5]  # Return

    finally:
        conn.close()
