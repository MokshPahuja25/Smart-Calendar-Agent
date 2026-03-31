# 📅 Smart Calendar AI Agent (HITL)
An AI-powered scheduling assistant built during the Gen AI Academy APAC Edition, hosted by Google Cloud and Hack2Skill. This agent uses Google Gemini to process natural language and features a unique Human-in-the-Loop (HITL) architecture to prevent automated scheduling conflicts.

## 🚀 Overview
Traditional chatbots often struggle with messy human language or blindly overwrite calendar data. This project solves that by using a Large Language Model (LLM) to understand intent and a validation layer that pauses for human confirmation whenever a scheduling overlap is detected.

## ✨ Key Features
Natural Language Processing: Processes conversational inputs like "Remind me to call Mom at 2 PM" using Gemini 2.5 Flash.

Intelligent Conflict Detection: Automatically cross-references new requests against a SQLite database.

Human-in-the-Loop (HITL) Protocol: If a slot is taken, the agent halts execution and requests user intervention via a dedicated /resolve-conflict endpoint.

Real-time Dashboard: A sleek Streamlit interface to view and manage the current schedule.

Cloud-Native Deployment: Fully containerized and hosted on Google Cloud Run.

## 🛠️ Tech Stack
LLM Engine: Google Gemini 2.5 Flash

Backend Framework: FastAPI (Python)

Frontend UI: Streamlit

Database: SQLite

Infrastructure: Google Cloud Run (Serverless)

## 🏗️ Architecture & Process Flow
Input: User provides unstructured text.

Extraction: Gemini extracts Task Name and Time Slot.

Validation: System checks the database for existing entries at that time.

Conflict Handling: * If Free: Task is booked immediately.

If Busy: System returns a CONFLICT status and waits for user resolution.

Visualization: Streamlit fetches data from the API to display a clean schedule table.

## 🔮 Future Scope & Known Limitations

While this prototype successfully demonstrates the core Human-in-the-Loop (HITL) architecture, the following upgrades are planned for production readiness:

* **Persistent Database Migration:** Currently, the system uses a local SQLite database, which resets when the serverless Cloud Run instance spins down to save resources. The next planned step is migrating to **Google Cloud SQL (PostgreSQL)** for permanent, scalable state management.
* **Full Date & Timezone Support:** Expanding the Gemini NLP extraction to handle specific calendar dates (not just daily time slots) and standardizing all backend times to UTC to support users across different global timezones.
* **Task Deletion & Modification:** Implementing a new conversational intent that allows users to seamlessly delete or modify existing calendar events via chat (e.g., *"Cancel my 2 PM meeting"* or *"Move the marketing sync to tomorrow"*).

## 🎖 Acknowledgments
Special thanks to the following organizations for the opportunity and resources provided during the **Gen AI Academy APAC Edition**:

* **Google Cloud** [@googlecloud](https://github.com/googlecloud) 
* **Hack2Skill** [Hack2Skill](https://hack2skill.com/)
