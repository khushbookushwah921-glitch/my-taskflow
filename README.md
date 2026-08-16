# TaskFlow — Full-Stack AI-Assisted Task Management Platform

TaskFlow is a full-stack task and project management platform designed to help users organize projects, manage tasks, track progress, and quickly find tasks using efficient algorithms.

The application includes secure user authentication, project management, task management, statistics, algorithm-powered search and sorting, and an AI-assisted Quick-Add feature.

---

## Features

### 1. User Authentication
- User registration
- Secure password hashing
- User login
- JWT-based authentication
- Protected project and task APIs
- Current user information endpoint

### 2. Project Management
- Create projects
- View projects
- Delete projects
- Projects are associated with the authenticated user
- Users can only access their own projects

### 3. Task Management
- Create tasks inside projects
- View all tasks
- View a task by ID
- Update task status
- Delete tasks
- Task priority support:
  - Low
  - Medium
  - High
- Due date support
- Task description support

### 4. Task Search

TaskFlow supports two search algorithms:

- Binary Search
- Linear Search

Binary Search first sorts task records and then searches efficiently.

The search API allows the algorithm to be selected using:

```text
algo=binary