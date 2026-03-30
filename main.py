from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# --- SETUP ---
# Put your Gemini API key here inside the quotes
os.environ["GOOGLE_API_KEY"] = "AIzaSyDX-bzGkAdUbCiEbovBPle1BI90iR8J4Ns"

app = FastAPI(title="Smart Calendar Agent")

# Initialize the AI translator tool
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# --- DATA FORMATS ---
class TaskRequest(BaseModel):
    user_input: str

class ConflictResolution(BaseModel):
    time_slot: str
    winner_task: str
    displaced_task: str
    new_time_for_displaced: str

# --- HELPER FUNCTION ---
def check_calendar(time_slot: str):
    """Checks the database to see if a time slot is taken."""
    conn = sqlite3.connect('my_calendar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT task_name FROM schedule WHERE time_slot = ?', (time_slot,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# --- ENDPOINT 1: The AI Agent Ingests the Task ---
@app.post("/schedule-task")
def schedule_task(request: TaskRequest):
    # 1. AI parses the messy human input
    prompt = f"""
    Extract the task name and the time from this sentence: "{request.user_input}"
    Return ONLY a comma-separated string like this: Task Name, Time
    Example output: Client Meeting, 10:00 AM
    """
    ai_response = llm.invoke(prompt).content.strip()
    
    try:
        new_task, requested_time = [item.strip() for item in ai_response.split(',')]
    except:
        return {"error": "AI could not understand the time or task. Try again!"}

    # 2. Check Database for Conflicts
    existing_task = check_calendar(requested_time)

    # 3. Handle the logic
    if existing_task:
        # CONFLICT DETECTED! Ask the user what to do.
        return {
            "status": "CONFLICT",
            "message": f"Wait! You already have '{existing_task}' scheduled at {requested_time}.",
            "action_required": "Please use the /resolve-conflict endpoint to decide which task gets this slot, and provide a new time for the other one."
        }
    else:
        # FREE SLOT! Book it.
        conn = sqlite3.connect('my_calendar.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO schedule (time_slot, task_name) VALUES (?, ?)', (requested_time, new_task))
        conn.commit()
        conn.close()
        return {"status": "SUCCESS", "message": f"Booked '{new_task}' at {requested_time}."}

# --- ENDPOINT 2: Human-in-the-Loop Resolution ---
@app.post("/resolve-conflict")
def resolve_conflict(resolution: ConflictResolution):
    conn = sqlite3.connect('my_calendar.db')
    cursor = conn.cursor()
    
    # 1. Update the disputed slot with the winner
    cursor.execute('UPDATE schedule SET task_name = ? WHERE time_slot = ?', (resolution.winner_task, resolution.time_slot))
    
    # 2. Book the new slot for the loser
    try:
        cursor.execute('INSERT INTO schedule (time_slot, task_name) VALUES (?, ?)', (resolution.new_time_for_displaced, resolution.displaced_task))
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": f"Failed! {resolution.new_time_for_displaced} is ALSO taken!"}
    
    conn.commit()
    conn.close()
    
    return {
        "status": "RESOLVED", 
        "message": f"Done! {resolution.time_slot} is now '{resolution.winner_task}'. The displaced task '{resolution.displaced_task}' is moved to {resolution.new_time_for_displaced}."
    }

# --- ENDPOINT 3: View the Calendar ---
@app.get("/view-calendar")
def view_calendar():
    conn = sqlite3.connect('my_calendar.db')
    cursor = conn.cursor()
    
    # Grab everything from the schedule table
    cursor.execute('SELECT time_slot, task_name FROM schedule')
    rows = cursor.fetchall()
    conn.close()
    
    # Format the data into a clean list of dictionaries
    schedule_list = [{"Time": row[0], "Task": row[1]} for row in rows]
    
    return {"status": "SUCCESS", "schedule": schedule_list}