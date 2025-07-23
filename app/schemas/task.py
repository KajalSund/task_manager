# app/schemas/task.py
from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
