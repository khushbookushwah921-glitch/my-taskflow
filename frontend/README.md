# TaskFlow

TaskFlow is a full-stack task management application that helps users manage projects and tasks efficiently.

## 🚀 Features

- User registration and login
- JWT-based authentication
- Create and manage projects
- Create tasks under projects
- Set task priority
- Set task due dates
- Mark tasks as completed or pending
- Delete tasks
- Search tasks
- Filter tasks by priority
- Dashboard statistics
- Responsive dashboard UI

## 🛠️ Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- FastAPI
- Python
- SQLAlchemy
- Pydantic
- JWT Authentication

### Database
- SQLite

## 📂 Project Structure

```text
TaskFlow/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   └── auth.py
│   └── venv/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md

## ▶️ How to Run

### Backend

Open a terminal and navigate to the backend folder:

```bash
cd TaskFlow/backend