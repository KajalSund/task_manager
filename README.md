# Task Manager

Task Manager is a lightweight, containerized web application built with **FastAPI**, **PostgreSQL**, and **Docker**, designed for managing tasks with user authentication. It supports secure login, role-based access, and full CRUD operations for task management. The application is fully automated with **GitHub Actions CI/CD** and deployed to Kubernetes using **Helm** and **ArgoCD**.

---

## Features

- User Authentication – Secure JWT-based login & registration
- Role Management – Support for viewer and editor roles
- Task Management – Create, Read, Update, Delete (CRUD) operations
- Dockerized Deployment – Ready-to-run using Docker & Kubernetes
- CI/CD Pipeline – Automated build & deployment via GitHub Actions + ArgoCD
- Helm-based K8s Deployment – Easy scaling & management on Kubernetes

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

### Backend
- **FastAPI** – REST API framework
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM for database interaction
- **Pydantic** – Data validation and serialization
- **Uvicorn** – ASGI server
- **Docker** – Containerization
- **GitHub Actions** – CI automation
- **Helm** – Kubernetes packaging
- **Kubernetes (k3s) Clusters** – Deployment environment
- **ArgoCD** – Continuous deployment

### Frontend
- **HTML5** – Page structure
- **CSS3** – Styling
- **Bootstrap** – Responsive UI design
- **JavaScript (Vanilla)** – Client-side logic


## Developer Notes
Run locally (without Docker):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```


## Argo CD Setup
Step 1: Install Argo CD on your k3s cluster
Run these commands on your local terminal with kubectl context set to your k3s cluster:
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
Step 2: Access Argo CD UI
By default, Argo CD API server is not exposed externally. You can port-forward to access UI locally:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Open https://localhost:8080 in your browser.

Step 3: Get Argo CD initial admin password
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```
Use username: admin and the decoded password to log in.

Step 4: Connect your Git repository to Argo CD
You can connect your GitHub repository:

Via UI: Navigate to Settings → Repositories and add your repo URL.

Via CLI:
```bash
argocd repo add <REPO_URL> --username <USERNAME> --password <TOKEN>
```

Step 5: Create an Argo CD Application
You can create the application either via UI or CLI:

```bash
argocd app create task-manager \
  --repo <REPO_URL> \
  --path helm \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
```
Step 6: Sync your Application:
Click Sync in the Argo CD UI.

This will deploy the manifests from your Git repository to the k3s cluster.
## Accessing the Application
- Using Port Forwarding
```bash
kubectl port-forward svc/task-manager-service 8090:80
```
- Access the app locally in browser:
http://localhost:8090
## Task Manager API – Endpoint Summary
| Method | Endpoint           | Description                    | Auth Required |
| ------ | ------------------ | ------------------------------ | ------------- |
| `POST` | `/signup`          | Register a new user            | No          |
| `POST` | `/login`           | Authenticate and get JWT token | No          |
| `GET`  | `/tasks/`          | Get list of tasks for user     | Yes         |
| `POST` | `/tasks/`          | Create a new task              | Yes         |
| `PUT`  | `/tasks/{task_id}` | Update a task                  | Yes         |
