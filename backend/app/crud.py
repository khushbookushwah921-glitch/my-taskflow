from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import hash_password, verify_password
from sqlalchemy import func

# ---------- Users ----------

def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(
       models.User.email == user.email
    ).first()

    if existing_user:
        return None
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_users(db: Session):
    return db.query(models.User).all()


# ---------- Projects ----------

def create_project(db: Session, project: schemas.ProjectCreate, owner_id: int):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        owner_id=owner_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

def get_projects(db: Session, owner_id: int):
    return db.query(models.Project).filter(
        models.Project.owner_id == owner_id
    ).all()

def delete_project(
    db: Session,
    project_id: int,
    owner_id: int
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == owner_id
    ).first()

    if project is None:
        return None

    # Delete tasks belonging to this project first
    db.query(models.Task).filter(
        models.Task.project_id == project_id
    ).delete(synchronize_session=False)

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}
# ---------- Tasks ----------

def create_task(
    db: Session,
    task: schemas.TaskCreate,
    owner_id: int
):
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id,
        models.Project.owner_id == owner_id
    ).first()

    if project is None:
        return None

    db_task = models.Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(db: Session, owner_id: int):
    return db.query(models.Task).join(
        models.Project
    ).filter(
        models.Project.owner_id == owner_id
    ).all()


def update_task_status(
    db: Session,
    task_id: int,
    status: str,
    owner_id: int
):
    task = db.query(models.Task).join(
        models.Project
    ).filter(
        models.Task.id == task_id,
        models.Project.owner_id == owner_id
    ).first()

    if task is None:
        return None

    task.status = status
    db.commit()
    db.refresh(task)

    return task

def delete_task(
    db: Session,
    task_id: int,
    owner_id: int
):
    task = db.query(models.Task).join(
        models.Project
    ).filter(
        models.Task.id == task_id,
        models.Project.owner_id == owner_id
    ).first()

    if task is None:
        return None

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user

def get_task_by_id(
    db: Session,
    task_id: int,
    owner_id: int
):
    return db.query(models.Task).join(
        models.Project
    ).filter(
        models.Task.id == task_id,
        models.Project.owner_id == owner_id
    ).first()    

def get_project_statistics(
    db: Session,
    owner_id: int
):
    results = db.query(
        models.Project.id.label("project_id"),
        models.Project.name.label("project_name"),
        func.count(models.Task.id).label("task_count")
    ).outerjoin(
        models.Task,
        models.Project.id == models.Task.project_id
    ).filter(
        models.Project.owner_id == owner_id
    ).group_by(
        models.Project.id,
        models.Project.name
    ).all()

    statistics = []

    for project_id, project_name, task_count in results:
        status_results = db.query(
            models.Task.status,
            func.count(models.Task.id)
        ).filter(
            models.Task.project_id == project_id
        ).group_by(
            models.Task.status
        ).all()

        status_counts = {
            "pending": 0,
            "in_progress": 0,
            "completed": 0
        }

        for status, count in status_results:
            if status in status_counts:
                status_counts[status] = count

        statistics.append({
            "project_id": project_id,
            "project_name": project_name,
            "task_count": task_count,
            "status_counts": status_counts
        })

    return statistics    

def get_project_by_id(db, project_id, user_id):
    return (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.owner_id == user_id
        )
        .first()
    )