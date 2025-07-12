from fastapi import FastAPI
from app.routers import auth, task
from app.database import engine, Base
# Import all models here so they are registered with Base
from app.models.user import User
from app.models.task import Task
from sqlalchemy.exc import OperationalError

app = FastAPI()
Base.metadata.create_all(bind=engine)
try:
    print("✅ Tables created successfully.")
except OperationalError as e:
    print("❌ Table creation error:", e)

app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
def root():
    return {"message": "Task Manager API running!"}
