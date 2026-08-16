from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import time

from app.database import Base, engine, get_db
from app import models, schemas, crud
from app.auth import create_access_token, get_current_user


app = FastAPI(title="TaskFlow API")


# -----------------------------
# DATABASE
# -----------------------------

Base.metadata.create_all(bind=engine)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# -----------------------------
# REQUEST LOGGING MIDDLEWARE
# -----------------------------

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {process_time:.2f} ms"
    )

    return response


# -----------------------------
# HOME
# -----------------------------

@app.get("/")
def home():
    return {"message": "Welcome to TaskFlow API"}


# -----------------------------
# USERS
# -----------------------------

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=201
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    created_user = crud.create_user(db, user)

    if created_user is None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return created_user


@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return crud.get_users(db)


# -----------------------------
# LOGIN
# -----------------------------

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    authenticated_user = crud.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not authenticated_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": authenticated_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -----------------------------
# CURRENT USER
# -----------------------------

@app.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


# -----------------------------
# PROJECTS
# -----------------------------

@app.post(
    "/projects",
    response_model=schemas.ProjectResponse,
    status_code=201
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_project(
        db,
        project,
        current_user.id
    )


@app.get(
    "/projects",
    response_model=list[schemas.ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_projects(
        db,
        current_user.id
    )


@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = crud.delete_project(
        db,
        project_id,
        current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return deleted


# -----------------------------
# TASKS - CREATE
# -----------------------------

@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=201
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    created_task = crud.create_task(
        db,
        task,
        current_user.id
    )

    if created_task is None:
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this project"
        )

    return created_task


# -----------------------------
# TASKS - LIST
# -----------------------------

@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_tasks(
        db,
        current_user.id
    )


# -----------------------------
# TASKS - GET BY ID
# -----------------------------

@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = crud.get_task_by_id(
        db,
        task_id,
        current_user.id
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# -----------------------------
# TASKS - UPDATE
# -----------------------------

@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    task: schemas.TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_task = crud.update_task_status(
        db,
        task_id,
        task.status,
        current_user.id
    )

    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task


# -----------------------------
# TASKS - DELETE
# -----------------------------

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = crud.delete_task(
        db,
        task_id,
        current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return deleted


# -----------------------------
# PROJECT STATISTICS
# -----------------------------

@app.get("/projects/statistics")
def project_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_project_statistics(
        db,
        current_user.id
    )