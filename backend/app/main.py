from pydantic import BaseModel
from app.algorithms import insertion_sort, binary_search, linear_search
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import time
from app.quick_add import parse_quick_add
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
    sort: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tasks = crud.get_tasks(db, current_user.id)

    if sort == "priority":
        records = [
            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date,
                "project_id": task.project_id,
                "status": task.status
            }
            for task in tasks
        ]

        priority_rank = {
            "low": 1,
            "medium": 2,
            "high": 3
        }

        for record in records:
            record["_priority_rank"] = priority_rank.get(
                record["priority"], 2
            )

        insertion_sort(records, "_priority_rank")

        for record in records:
            record.pop("_priority_rank", None)

        return records

    return tasks


# -----------------------------
# TASKS - GET BY ID
# -----------------------------
@app.get("/tasks/search", response_model=schemas.TaskResponse)
def search_tasks(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tasks = crud.get_tasks(db, current_user.id)

    records = [
        {
            "id": task.id,
            "title": task.title
        }
        for task in tasks
    ]

    if algo == "binary":
        insertion_sort(records, "title")
        index = binary_search(records, title, "title")

    elif algo == "linear":
        index = linear_search(records, title, "title")

    else:
        raise HTTPException(
            status_code=422,
            detail="algo must be binary or linear"
        )

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_id = records[index]["id"]

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

# -----------------------------
# AI QUICK-ADD
# -----------------------------

class QuickAddRequest(BaseModel):
    description: str
    project_id: int


@app.post(
    "/tasks/quick-add",
    response_model=schemas.TaskResponse,
    status_code=201
)
def quick_add_task(
    data: QuickAddRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check project belongs to current user
    project = crud.get_project_by_id(
        db,
        data.project_id,
        current_user.id
    )

    if project is None:
        raise HTTPException(
            status_code=422,
            detail="Project does not exist"
        )

    parsed = parse_quick_add(data.description)

    task_data = schemas.TaskCreate(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=parsed["due_date_hint"],
        project_id=data.project_id
    )

    created_task = crud.create_task(
        db,
        task_data,
        current_user.id
    )

    if created_task is None:
        raise HTTPException(
            status_code=422,
            detail="Unable to create task"
        )

    return created_task