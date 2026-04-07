import wikipedia
from mcp.server.fastmcp import FastMCP
from google.cloud import datastore
from datetime import datetime

# Initialize Datastore with your NAMED database
def get_db():
    return datastore.Client(
        project=os.environ.get("PROJECT_ID", "studymate-492606"),
        database="studymate-db"
    )
mcp = FastMCP("StudymateAI")

# --- 1. RESEARCH ---
@mcp.tool()
def research_topic(query: str) -> str:
    """Searches Wikipedia for facts about a study topic."""
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return f"Could not find specific Wikipedia data for {query}."

# --- 2. TASK MANAGEMENT (Add, List, Update) ---
@mcp.tool()
def add_task(title: str, priority: str = "medium") -> str:
    """Adds a new task."""
    key = db.key("Task")
    task = datastore.Entity(key=key)
    task.update({"title": title, "priority": priority, "status": "pending", "created": datetime.utcnow()})
    db.put(task)
    return f"Task '{title}' added."

@mcp.tool()
def list_tasks() -> str:
    """Retrieves all pending tasks so you can manage them."""
    query = db.query(kind="Task")
    results = list(query.fetch())
    if not results: return "You have no tasks currently."
    
    task_list = "\n".join([f"- [{t['status']}] {t['title']} ({t['priority']} priority)" for t in results])
    return f"Current Tasks:\n{task_list}"

@mcp.tool()
def complete_task(title: str) -> str:
    """Marks a specific task as 'completed'."""
    query = db.query(kind="Task")
    query.add_filter("title", "=", title)
    results = list(query.fetch())
    if not results: return f"Task '{title}' not found."
    
    task = results[0]
    task["status"] = "completed"
    db.put(task)
    return f"Task '{title}' is now marked as completed!"

# --- 3. SCHEDULING (Add, View Schedule) ---
@mcp.tool()
def schedule_session(name: str, time: str) -> str:
    """Schedules a study session."""
    key = db.key("Event")
    event = datastore.Entity(key=key)
    event.update({"name": name, "time": time})
    db.put(event)
    return f"Event '{name}' scheduled for {time}."

@mcp.tool()
def view_schedule() -> str:
    """Shows all upcoming scheduled sessions."""
    query = db.query(kind="Event")
    results = list(query.fetch())
    if not results: return "Your schedule is currently empty."
    
    events = "\n".join([f"- {e['name']} at {e['time']}" for e in results])
    return f"Upcoming Schedule:\n{events}"

if __name__ == "__main__":
    mcp.run()