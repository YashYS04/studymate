import os
import wikipedia
import google.cloud.logging
from datetime import datetime
from google.cloud import datastore
from google.adk.agents import LlmAgent

# --- 1. SETUP CLOUD LOGGING ---
try:
    logging_client = google.cloud.logging.Client()
    logging_client.setup_logging()
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO)

# --- 2. CONFIGURATION ---
PROJECT_ID = "studymate-492606"
DATABASE_NAME = "studymate-db"

# --- 3. TOOLS DEFINITION ---

# -- RESEARCH TOOL --
def research_topic(query: str) -> str:
    """Searches Wikipedia for factual summaries about a specific study topic."""
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return f"No Wikipedia data found for {query}."

# -- TASK MANAGEMENT TOOLS --
def add_task(title: str, priority: str = "medium") -> str:
    """Saves a new to-do task to the cloud database."""
    db = datastore.Client(project=PROJECT_ID, database=DATABASE_NAME)
    key = db.key("Task")
    task = datastore.Entity(key=key)
    task.update({"title": title, "priority": priority, "status": "pending", "created": datetime.utcnow()})
    db.put(task)
    return f"Task '{title}' saved to your list."

def list_tasks() -> str:
    """Retrieves and lists all pending tasks from your database."""
    db = datastore.Client(project=PROJECT_ID, database=DATABASE_NAME)
    query = db.query(kind="Task")
    query.add_filter("status", "=", "pending")
    results = list(query.fetch())
    if not results: return "You have no pending tasks."
    return "Current Tasks:\n" + "\n".join([f"- {t['title']} ({t['priority']})" for t in results])

# -- NOTE MANAGEMENT TOOLS --
def save_note(topic: str, content: str) -> str:
    """Saves a research note or summary for a specific topic."""
    db = datastore.Client(project=PROJECT_ID, database=DATABASE_NAME)
    key = db.key("Note")
    note = datastore.Entity(key=key)
    note.update({"topic": topic, "content": content, "timestamp": datetime.utcnow()})
    db.put(note)
    return f"Note on '{topic}' saved successfully."

def list_notes() -> str:
    """Lists the topics of all saved notes in your notebook."""
    db = datastore.Client(project=PROJECT_ID, database=DATABASE_NAME)
    query = db.query(kind="Note")
    results = list(query.fetch())
    if not results: return "Your notebook is currently empty."
    return "Saved Notes:\n" + "\n".join([f"- {n['topic']}" for n in results])

def edit_note(topic: str, new_content: str) -> str:
    """Updates the content of an existing note based on its topic name."""
    db = datastore.Client(project=PROJECT_ID, database=DATABASE_NAME)
    query = db.query(kind="Note")
    query.add_filter("topic", "=", topic)
    results = list(query.fetch())
    if not results: return f"Could not find a note with the topic '{topic}'."
    
    note = results[0]
    note["content"] = new_content
    note["updated_at"] = datetime.utcnow()
    db.put(note)
    return f"Note on '{topic}' has been updated."

def delete_note(topic: str) -> str:
    """Removes a specific note from your notebook using its topic name."""
    db = datastore.Client(project=PROJECT_ID, database=DATABASE_NAME)
    query = db.query(kind="Note")
    query.add_filter("topic", "=", topic)
    results = list(query.fetch())
    if not results: return f"Could not find a note with the topic '{topic}'."
    
    db.delete(results[0].key)
    return f"Note on '{topic}' has been deleted."

# -- SCHEDULING TOOLS --
def schedule_event(event_name: str, date_time: str) -> str:
    """Schedules a study session, exam, or deadline in the calendar."""
    db = datastore.Client(project=PROJECT_ID, database=DATABASE_NAME)
    key = db.key("Event")
    event = datastore.Entity(key=key)
    event.update({"name": event_name, "time": date_time})
    db.put(event)
    return f"Successfully scheduled {event_name} for {date_time}."

def view_schedule() -> str:
    """Shows all upcoming sessions and events from your calendar."""
    db = datastore.Client(project=PROJECT_ID, database=DATABASE_NAME)
    query = db.query(kind="Event")
    results = list(query.fetch())
    if not results: return "Your schedule is clear."
    return "Upcoming Events:\n" + "\n".join([f"- {e['name']} at {e['time']}" for e in results])

# --- 4. AGENT INTEGRATION ---

instruction = """
You are StudyMate AI. 
- Use 'research_topic' for any factual or academic questions.
- Use 'add_task' and 'list_tasks' to manage to-dos.
- Use 'save_note', 'list_notes', 'edit_note', and 'delete_note' to manage your notebook.
- Use 'schedule_event' and 'view_schedule' for calendar and sessions.
Always ask for clarification if a topic name is unclear when editing or deleting.
"""

root_agent = LlmAgent(
    name="studymate_agent",
    model="gemini-2.5-flash",
    instruction=instruction,
    tools=[
        research_topic, 
        add_task, 
        list_tasks, 
        save_note, 
        list_notes, 
        edit_note, 
        delete_note, 
        schedule_event, 
        view_schedule
    ]
)