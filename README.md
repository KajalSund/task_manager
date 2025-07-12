# Task Manager API

A simple Task Manager backend application built using **FastAPI**, **PostgreSQL**, and **Docker**. It supports user authentication and CRUD operations for task management.

---

## Features

- User registration & login (JWT auth)
- Create, read, update, and delete tasks
- Task ownership and user roles (viewer/editor)
- Dockerized setup for easy deployment


---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Kajal-Sund/task_manager.git
cd task_manager
```
docker-compose up --build
App runs at: http://localhost:8000

## API Endpoints
POST /signup – Register user

POST /login – Get JWT token

GET /tasks – List tasks

POST /tasks – Create task

PUT /tasks/{id} – Update task

DELETE /tasks/{id} – Delete task

All task routes require JWT Authorization header: Bearer <token>
## Tech Stack
FastAPI

PostgreSQL

Docker

SQLAlchemy

Pydantic

Uvicorn

## Developer Notes
Run locally (without Docker):
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```