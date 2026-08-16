# TaskFlow — Full-Stack AI-Assisted Task Management Platform

TaskFlow is a full-stack task and project management platform built with FastAPI, SQLAlchemy, SQLite, React, and JavaScript.

It provides secure authentication, project and task management, task statistics, algorithm-powered sorting and searching, and an AI-assisted Quick-Add feature using a deterministic local mock parser.

---

## 1. Features

### Authentication

* User registration
* Secure password hashing
* JWT-based authentication
* Protected project and task APIs
* Current-user information endpoint

### Project Management

* Create projects
* List projects
* Get project by ID
* Delete projects
* User-specific project access

### Task Management

* Create tasks
* List tasks
* Get task by ID
* Update task status
* Delete tasks
* Priority support: low, medium, high
* Due-date support
* Task description support

### Statistics

TaskFlow provides project/task statistics including:

* Total tasks
* Pending tasks
* Completed tasks
* Progress information

### Algorithms

The project implements:

* Insertion Sort
* Linear Search
* Binary Search
* Algorithm benchmarking

### AI Quick-Add

Quick-Add accepts natural-language task descriptions and converts them into structured task data.

Example:

```text
Finish the final report high priority tomorrow
```

The parser extracts:

* Task title
* Priority
* Due-date hint

The required implementation is a deterministic mock parser. It requires:

* No API key
* No paid service
* No network request

---

# 2. Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* JWT
* Passlib
* bcrypt

## Frontend

* React
* JavaScript
* HTML
* CSS
* Fetch API
* LocalStorage

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
```

---

# 4. Environment Setup

## Prerequisites

* Python 3.10+
* Node.js and npm
* Git

## Create virtual environment

From the project root:

```bash
python -m venv venv
```

### Windows

```cmd
venv\Scripts\activate
```

### Install backend dependencies

```bash
pip install -r requirements.txt
```

---

# 5. Running the Application

TaskFlow runs as two local services.

## Start the backend

Open Terminal 1:

```cmd
cd C:\Users\Hp\OneDrive\Desktop\TaskFlow
venv\Scripts\activate
cd backend
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## Start the frontend

Open Terminal 2:

```cmd
cd C:\Users\Hp\OneDrive\Desktop\TaskFlow\frontend
npm install
npm run dev
```

Open the URL displayed by Vite, normally:

```text
http://localhost:5173
```

The frontend communicates with the FastAPI backend.

---

# 6. API Endpoints

All protected endpoints require:

```text
Authorization: Bearer <JWT_TOKEN>
```

## Authentication

### POST `/register`

Creates a new user.

Example request:

```json
{
  "name": "Khushboo",
  "email": "user@example.com",
  "password": "password123"
}
```

Example response:

```json
{
  "id": 1,
  "name": "Khushboo",
  "email": "user@example.com"
}
```

### POST `/login`

Authenticates a user and returns a JWT token.

Example request:

```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

Example response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### GET `/users/me`

Returns the authenticated user's information.

Example response:

```json
{
  "id": 1,
  "name": "Khushboo",
  "email": "user@example.com"
}
```

---

# 7. Project Endpoints

## POST `/projects`

Creates a project.

Example request:

```json
{
  "name": "TaskFlow Development",
  "description": "Build the TaskFlow platform"
}
```

Example response:

```json
{
  "id": 1,
  "name": "TaskFlow Development",
  "description": "Build the TaskFlow platform"
}
```

## GET `/projects`

Lists projects belonging to the authenticated user.

Example response:

```json
[
  {
    "id": 1,
    "name": "TaskFlow Development",
    "description": "Build the TaskFlow platform"
  }
]
```

## GET `/projects/{project_id}`

Gets a project by ID.

Example:

```text
GET /projects/1
```

Example response:

```json
{
  "id": 1,
  "name": "TaskFlow Development",
  "description": "Build the TaskFlow platform"
}
```

## DELETE `/projects/{project_id}`

Deletes a project.

Example:

```text
DELETE /projects/1
```

Example response:

```json
{
  "message": "Project deleted successfully"
}
```

---

# 8. Task Endpoints

## POST `/tasks`

Creates a task.

Example request:

```json
{
  "title": "Complete final report",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1,
  "description": "Finish and review the final report"
}
```

Example response:

```json
{
  "title": "Complete final report",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1,
  "id": 1,
  "status": "pending"
}
```

## GET `/tasks`

Lists tasks.

Example response:

```json
[
  {
    "title": "Complete final report",
    "priority": "high",
    "due_date": "tomorrow",
    "project_id": 1,
    "id": 1,
    "status": "pending"
  }
]
```

## GET `/tasks/{task_id}`

Gets a task by ID.

Example:

```text
GET /tasks/1
```

Example response:

```json
{
  "title": "Complete final report",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1,
  "id": 1,
  "status": "pending"
}
```

## PUT `/tasks/{task_id}`

Updates a task.

Example request:

```json
{
  "status": "completed"
}
```

Example response:

```json
{
  "title": "Complete final report",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 1,
  "id": 1,
  "status": "completed"
}
```

## DELETE `/tasks/{task_id}`

Deletes a task.

Example:

```text
DELETE /tasks/1
```

Example response:

```json
{
  "message": "Task deleted successfully"
}
```

---

# 9. Statistics

## GET `/projects/{project_id}/stats`

Returns task statistics for a project.

Example:

```text
GET /projects/1/stats
```

Example response:

```json
{
  "total": 5,
  "pending": 2,
  "completed": 3
}
```

---

# 10. Sorted Task List

## GET `/tasks?sort=priority`

Returns tasks sorted by priority.

Example:

```text
GET /tasks?sort=priority
```

Example response:

```json
[
  {
    "title": "Fix documentation",
    "priority": "low",
    "due_date": null,
    "project_id": 1,
    "id": 1,
    "status": "pending"
  },
  {
    "title": "Complete final report",
    "priority": "medium",
    "due_date": "tomorrow",
    "project_id": 1,
    "id": 2,
    "status": "completed"
  }
]
```

The implementation uses the project's sorting algorithm for ordered task data.

---

# 11. Task Search

## GET `/tasks/search`

Searches tasks by title.

The algorithm can be selected using the `algo` query parameter.

### Linear Search

```text
GET /tasks/search?title=complete final testing&algo=linear
```

Example response:

```json
[
  {
    "title": "complete final testing",
    "priority": "medium",
    "due_date": null,
    "project_id": 3,
    "id": 3,
    "status": "completed"
  }
]
```

### Binary Search

```text
GET /tasks/search?title=complete final testing&algo=binary
```

Example response:

```json
[
  {
    "title": "complete final testing",
    "priority": "medium",
    "due_date": null,
    "project_id": 3,
    "id": 3,
    "status": "completed"
  }
]
```

Both search approaches were tested successfully.

---

# 12. AI Quick-Add

## POST `/tasks/quick-add`

Creates a task from natural-language input.

Example request:

```json
{
  "text": "Finish the final report high priority tomorrow",
  "project_id": 2
}
```

Example response:

```json
{
  "title": "Finish the final report",
  "priority": "high",
  "due_date": "tomorrow",
  "project_id": 2,
  "id": 4,
  "status": "pending"
}
```

The parser works locally without API keys or network calls.

---

# 13. Algorithms and Complexity

## Insertion Sort

Insertion Sort builds a sorted sequence one element at a time.

### Complexity

* Best case: O(n)
* Average case: O(n²)
* Worst case: O(n²)
* Space: O(1)

It is useful for small datasets and nearly sorted data.

## Linear Search

Linear Search checks elements one by one until a matching task title is found.

### Complexity

* Best case: O(1)
* Average case: O(n)
* Worst case: O(n)
* Space: O(1)

It does not require the data to be sorted.

## Binary Search

Binary Search repeatedly divides sorted data into halves.

### Complexity

* Best case: O(1)
* Average case: O(log n)
* Worst case: O(log n)
* Space: O(1) for the iterative implementation

Binary Search requires sorted data, so TaskFlow sorts task records before using this search strategy.

---

# 14. Benchmark Results

The project includes `benchmark.py` for comparing algorithm performance.

The benchmark was executed using multiple dataset sizes.

Example benchmark output:

```text
TaskFlow Algorithm Benchmark
============================================================

DATA SIZE: 10
------------------------------------------------------------
Insertion Sort comparisons: 45
```

The benchmark demonstrates that insertion sort performs more comparisons as the input size grows, matching its expected O(n²) worst-case behavior.

The search tests were also verified using:

```text
PASS: binary_search_count
PASS: linear_search_count
```

---

# 15. AI Prompting Technique and Rationale

The Quick-Add feature is designed around a structured extraction approach.

The input is natural language, while the application needs structured fields.

The parser therefore follows these steps:

1. Identify the main task title.
2. Detect priority keywords such as `low`, `medium`, or `high`.
3. Detect due-date hints such as `today`, `tomorrow`, or date expressions.
4. Remove recognized metadata from the task title.
5. Return a predictable structured object.
6. Use default values when optional information is missing.

This approach is deterministic and easy to test.

The required assignment implementation intentionally uses a mock parser so that:

* No API key is required.
* No network call is required.
* Results are reproducible.
* The feature can be tested offline.

---

# 16. Five AI Quick-Add Worked Examples

## Example 1

Input:

```text
Finish the final report high priority tomorrow
```

Parsed result:

```json
{
  "title": "Finish the final report",
  "priority": "high",
  "due_date": "tomorrow"
}
```

## Example 2

Input:

```text
Review project documentation low priority today
```

Parsed result:

```json
{
  "title": "Review project documentation",
  "priority": "low",
  "due_date": "today"
}
```

## Example 3

Input:

```text
Complete frontend testing high priority
```

Parsed result:

```json
{
  "title": "Complete frontend testing",
  "priority": "high",
  "due_date": null
}
```

## Example 4

Input:

```text
Update README medium priority tomorrow
```

Parsed result:

```json
{
  "title": "Update README",
  "priority": "medium",
  "due_date": "tomorrow"
}
```

## Example 5

Input:

```text
Check backend API
```

Parsed result:

```json
{
  "title": "Check backend API",
  "priority": "medium",
  "due_date": null
}
```

---

# 17. Testing

The project includes algorithm verification and API testing.

Algorithm verification:

```cmd
python check_algorithms.py
```

Expected successful checks include:

```text
PASS: binary_search_count
PASS: linear_search_count
```

Benchmark:

```cmd
python benchmark.py
```

The FastAPI Swagger interface can be used to test all API endpoints:

```text
http://127.0.0.1:8000/docs
```

---

# 18. Git Workflow

The repository contains feature-branch development and merge history.

Important branches include:

* `feature/algorithms-ai`
* `final-verification`
* `main`

The algorithms/AI feature branch contains multiple commits and was merged back into `main`.

The repository history can be inspected with:

```cmd
git --no-pager log --oneline --graph --all --decorate
```

---

# 19. Submission

This repository contains the complete TaskFlow project in a single public GitHub repository.

Repository:

https://github.com/khushbookushwah921-glitch/my-taskflow
