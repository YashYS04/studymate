# 🎓 StudyMate (Study AI)

**StudyMate** is a high-performance AI Academic Assistant built on the **Gemini 2.5 Flash** model. It serves as a centralized "Second Brain," transforming a standard chat interface into a fully functional research and organization suite.

---

## 🌟 Core Features

* **⚡ Zero-Latency Monolithic Architecture:** Designed to eliminate the "Connection Closed" and 5-second timeout errors common in standard MCP setups by using direct-function orchestration.
* **🧠 Intelligent Parallel Execution:** Leverages Gemini 2.0's reasoning to trigger multiple tools simultaneously (e.g., researching a topic and saving it as a note in a single turn).
* **📚 Persistent Cloud Memory:** Integrates directly with **Google Cloud Datastore** to ensure that all tasks, research notes, and schedules are saved permanently across sessions.
* **🔍 Grounded Fact Synthesis:** Combines AI creativity with real-time Wikipedia data to provide factual, citation-ready academic summaries.
* **🛠️ Full Data Lifecycle (CRUD):** Unlike simple bots, StudyMate Pro can **Create, Read, Update, and Delete** user data, allowing for true notebook management.

---

## 🛠️ The Toolset: What it Does

The agent is equipped with a specialized suite of Python-powered tools that it calls autonomously based on your requests:

### **1. Research & Knowledge**
* **`research_topic`**: Queries Wikipedia's live database to provide concise, 3-sentence factual summaries of any academic subject.

### **2. Notebook Management (Full CRUD)**
* **`save_note`**: Permanently archives research findings or lecture summaries into the cloud.
* **`list_notes`**: Retrieves a complete index of all topics currently stored in your cloud notebook.
* **`edit_note`**: Allows you to update the content of existing notes as you gather more information.
* **`delete_note`**: Cleans up your workspace by removing notes that are no longer needed.

### **3. Task & To-Do Organization**
* **`add_task`**: Saves new academic obligations with priority levels (High, Medium, Low).
* **`list_tasks`**: Fetches all pending to-dos so you never miss a deadline.

### **4. Scheduling & Planning**
* **`schedule_event`**: Records specific dates and times for exams, study groups, or project deadlines.
* **`view_schedule`**: Displays your upcoming academic calendar in a clear, chronological list.
  
<img width="1911" height="875" alt="project1" src="https://github.com/user-attachments/assets/fe5d86b1-bc28-4911-af5d-5235cae92a27" />

---
<img width="1906" height="868" alt="project3" src="https://github.com/user-attachments/assets/8bb8d9f7-01d8-4a35-ad90-16e24d09e754" />

## 🏗️ Technical Stack

| Component | Technology |
| :--- | :--- |
| **Model** | Gemini 2.5 Flash |
| **Orchestration** | Google Agent Development Kit (ADK) 1.14.0 |
| **Database** | Google Cloud Datastore |
| **Deployment** | Google Cloud Run (Serverless) |
| **Monitoring** | Google Cloud Logging |
| **Language** | Python 3.11 |

---

## 💡 Usage Scenarios

* **Complex Research:** *"Research 'Quantum Entanglement', save it as a note, and add a task to 'Review Quantum Notes' tomorrow."*
* **Organization:** *"What are my pending tasks for today? If I'm done with 'Math Homework', mark it as complete."*
* **Calendar Management:** *"Schedule my 'AI Finals' for April 25th at 10 AM and show me my full schedule."*
