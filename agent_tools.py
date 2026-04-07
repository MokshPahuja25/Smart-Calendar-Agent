import sqlite3

DB_NAME = 'my_calendar.db'

def add_new_task(task_name: str, priority: str = "Medium") -> str:
    """
    Use this tool to add a new task to the user's to-do list.
    Priority should be 'High', 'Medium', or 'Low'.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, priority) VALUES (?, ?)", (task_name, priority))
    conn.commit()
    conn.close()
    return f"Success: '{task_name}' added to tasks with {priority} priority."

def book_calendar_slot(time_slot: str, task_name: str) -> str:
    """
    Use this tool to book a calendar slot. 
    CRITICAL RULE: time_slot MUST be in strict 24-hour format (HH:MM). 
    If the user says '2' or '2 PM', you MUST convert it to '14:00' before calling this tool.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # HITL Conflict Check: See if the slot is taken
    cursor.execute("SELECT * FROM calendar WHERE time_slot = ?", (time_slot,))
    if cursor.fetchone():
        conn.close()
        return f"CONFLICT: {time_slot} is already booked. Ask the user if they want to resolve or overwrite."
        
    cursor.execute("INSERT INTO calendar (time_slot, task_name) VALUES (?, ?)", (time_slot, task_name))
    conn.commit()
    conn.close()
    return f"Success: '{task_name}' scheduled for {time_slot}."

def delete_calendar_slot(time_slot: str) -> str:
    """
    Use this tool to delete or cancel an existing calendar event.
    CRITICAL RULE: time_slot MUST be in strict 24-hour format (HH:MM).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calendar WHERE time_slot = ?", (time_slot,))
    conn.commit()
    conn.close()
    return f"Success: Event at {time_slot} has been deleted."