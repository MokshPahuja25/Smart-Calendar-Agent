import streamlit as st
import requests

# Put your live Cloud Run API link here (do NOT include /docs at the end)
API_URL = "https://smart-calendar-agent-761950427575.asia-south2.run.app" 

st.title("📅 Smart Calendar Agent")
st.write("Chat with your AI assistant to schedule tasks!")
# The Sidebar Dashboard
with st.sidebar:
    st.header("📊 Dashboard")
    st.write("Check your current schedule.")
    
    # When the user clicks this button...
    if st.button("📅 View Calendar Table"):
        # Make a GET request to your new API door
        response = requests.get(f"{API_URL}/view-calendar")
        
        if response.status_code == 200:
            data = response.json()
            schedule = data.get("schedule", [])
            
            if schedule:
                st.success("Your Schedule:")
                # This magically turns your data into a beautiful table!
                st.table(schedule) 
            else:
                st.info("Your calendar is completely empty!")
        else:
            st.error("Failed to connect to the database.")
    
    st.markdown("---")

# Store the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# The Chat Input Box
user_input = st.chat_input("Tell me what to schedule...")

if user_input:
    # 1. Show what the user typed
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Send the text to YOUR Brain (The Cloud Run API)
    response = requests.post(f"{API_URL}/schedule-task", json={"user_input": user_input})
    
    # 3. Read the AI's answer
    if response.status_code == 200:
        api_data = response.json()
        
        # If it's a success
        if api_data.get("status") == "SUCCESS":
            ai_reply = api_data["message"]
            
        # If there is a conflict
        elif api_data.get("status") == "CONFLICT":
            ai_reply = f"⚠️ **CONFLICT:** {api_data['message']} \n\n*Head to the API dashboard to resolve this using /resolve-conflict!*"
            
        else:
            ai_reply = "Hmm, I didn't understand that."
    else:
        ai_reply = "Error connecting to the Brain!"

    # 4. Show the AI's answer on the screen
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})