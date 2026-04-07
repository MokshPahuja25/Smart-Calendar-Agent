import os
from fastapi import FastAPI
import google.generativeai as genai
from pydantic import BaseModel

# 🔹 Import the Specialists (Tools) we just built!
from agent_tools import add_new_task, book_calendar_slot, delete_calendar_slot

# 1. Setup FastAPI 
app = FastAPI(title="Multi-Agent Productivity Assistant")

# Configure Gemini securely using the environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Define the Supervisor Identity (The Brain)
supervisor_instructions = """
You are the Executive Supervisor of a Multi-Agent Productivity System.
Your job is to manage the user's schedule and to-do list using your tools.

You have three specialists (tools) on your team:
1. add_new_task: Use this when the user wants to add something to their to-do list.
2. book_calendar_slot: Use this when a user wants to schedule an event. 
   CRITICAL: You must convert all times to 24-hour format (HH:MM) before using this tool. Assume PM if ambiguous (e.g., "2" means "14:00").
3. delete_calendar_slot: Use this when a user wants to cancel or remove an event.

INSTRUCTIONS:
- Break down the user's request. If they ask for multiple things (e.g., "Add a task AND schedule it"), use the tools sequentially.
- If a tool returns a CONFLICT message, stop and ask the user how they want to resolve it.
- Once the tools succeed, give the user a brief, friendly summary of what was accomplished.
"""

# Initialize the Manager with the tools and instructions
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=supervisor_instructions,
    tools=[add_new_task, book_calendar_slot, delete_calendar_slot] # Handing the tools to the Manager
)

# Start a chat session that allows the Manager to run the Python functions autonomously
chat = model.start_chat(enable_automatic_function_calling=True)

# 3. Define the API Request Body
class UserRequest(BaseModel):
    prompt: str

# 4. Create the API Endpoint
@app.post("/chat")
async def chat_endpoint(request: UserRequest):
    try:
        # Send the user's message to the Supervisor
        response = chat.send_message(request.prompt)
        return {"status": "success", "response": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Basic health check endpoint
@app.get("/")
def read_root():
    return {"message": "Supervisor Agent is Online."}

if __name__ == "__main__":
    import uvicorn
    # Cloud Run injects the PORT environment variable, defaulting to 8080
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)