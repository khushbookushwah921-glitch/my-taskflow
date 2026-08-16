# TaskFlow — Full-Stack AI-Assisted Task Management Platform

TaskFlow is a full-stack task and project management platform built with FastAPI, SQLAlchemy, SQLite, and a JavaScript frontend.

It provides secure authentication, project and task management, task statistics, algorithm-powered sorting and searching, and an AI-assisted Quick-Add feature using a deterministic mock parser with zero API keys and zero network calls.

---

## 1. Features

### Authentication
- User registration
- Secure password hashing
- JWT-based login
- Protected project and task endpoints
- Current-user endpoint

### Project Management
- Create projects
- List projects
- Delete projects
- User-specific project access

### Task Management
- Create tasks
- List tasks
- Get task by ID
- Update task status
- Delete tasks
- Priority: low, medium, high
- Due-date support
- Task description support

### Statistics
- Project-level task statistics
- Progress/status information

### Algorithms
- Insertion Sort
- Binary Search
- Linear Search
- Benchmark comparison

### AI Quick-Add
The Quick-Add feature accepts natural-language task descriptions and converts them into structured task data.

Example:

`Finish the report high priority tomorrow`

The parser extracts:
- title
- priority
- due-date hint

The required implementation uses a local mock parser and requires no API key or network connection.

---

# 2. Tech Stack

## Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn
- JWT authentication
- Passlib / bcrypt

## Frontend
- React
- JavaScript
- HTML
- CSS
- Fetch API
- LocalStorage

---

# 3. Project Structure

```text
TaskFlow/
├── backend/
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── database.py
│       ├── auth.py
│       └── algorithms.py
│
├── frontend/
│   └── src/
│       └── App.jsx
│
├── benchmark.py
├── check_algorithms.py
├── requirements.txt
└── README.md