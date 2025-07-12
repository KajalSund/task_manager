# app/routers/task.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.task.TaskOut)
def create_task(task: schemas.task.TaskCreate, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "editor":
        raise HTTPException(status_code=403, detail="Only editors can create tasks.")
    new_task = models.task.Task(**task.dict(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[schemas.task.TaskOut])
def get_tasks(db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return db.query(models.task.Task).filter(models.task.Task.owner_id == current_user.id).all()

@router.put("/{task_id}", response_model=schemas.task.TaskOut)
def update_task(task_id: int, task: schemas.task.TaskCreate, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    task_db = db.query(models.task.Task).filter(models.task.Task.id == task_id).first()
    if not task_db or task_db.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != "editor":
        raise HTTPException(status_code=403, detail="Only editors can update tasks.")
    for field, value in task.dict().items():
        setattr(task_db, field, value)
    db.commit()
    db.refresh(task_db)
    return task_db

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    task_db = db.query(models.task.Task).filter(models.task.Task.id == task_id).first()
    if not task_db or task_db.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != "editor":
        raise HTTPException(status_code=403, detail="Only editors can delete tasks.")
    db.delete(task_db)
    db.commit()
    return {"detail": "Task deleted"}
