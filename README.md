# AI SQL Generator (MCP)

An AI-powered SQL generator for the 'ccs-aquila-tahoe' database, featuring automatic business logic injection, context-aware chat, and a Reinforcement Learning from Human Feedback (RLHF) loop.

## 🚀 Features
- **Contextual SQL Generation**: Uses local Ollama (llama3) with a large context window (16k tokens).
- **Automatic CTE Injection**: Backend automatically prepends required business logic (CTEs) to every query.
- **RLHF Feedback Loop**: Users can rate queries (👍/👎), and "Good" examples are used for few-shot learning.
- **Chat History**: Supports follow-up questions.

## 📋 Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **Ollama** running locally with `llama3` model (`ollama run llama3`)

## 🛠️ How to Start

### 1. Start the Backend
Open a terminal and run:
```bash
cd sql_generator/backend
python3 main.py
```
*Runs on http://localhost:8000*

### 2. Start the Frontend
Open a **new** terminal tab/window and run:
```bash
cd sql_generator/frontend
npm run dev
```
*Runs on http://localhost:5173*

### 3. Access the App
Open your browser and go to: **http://localhost:5173**

---

## 🛑 How to Stop

To stop the servers, you can simply press `Ctrl+C` in the respective terminal windows.

If you need to force stop them (e.g., if they are running in the background), run:

```bash
# Find the Process IDs (PIDs)
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Kill the processes (replace <PID> with the actual numbers)
kill -9 <BACKEND_PID> <FRONTEND_PID>
```

## 📂 Project Structure
- `sql_generator/backend`: FastAPI server, Agent logic (`agent.py`), Feedback storage (`feedback.json`).
- `sql_generator/frontend`: React application, UI components.
- `sql_generator/mcp_server`: Schema and Business Logic definitions.
