# TaskFlow — Full-Stack AI-Assisted Task Management Platform

TaskFlow is a full-stack task and project management application built for
operations-engineering teams. It provides project management, task CRUD,
statistics, algorithm-powered sorting/search, and an AI-assisted Quick-Add
feature.

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

### Frontend
- HTML5
- CSS3
- JavaScript
- Fetch API
- LocalStorage

## Project Structure

```text
TaskFlow/
├── backend/
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── database.py
│       ├── algorithms.py
│       ├── check_algorithms.py
│       └── benchmark.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
└── README.md