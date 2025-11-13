# Mini Kanban – Full Stack Flask Demo

A small full stack project that demonstrates how I orchestrate backend, database, frontend, packaging, and Docker in a clean, production-like workflow.

This repo contains a simple **Kanban-style task manager** built with:

- **Backend:** Flask (Python)
- **Database:** SQLite (via SQLAlchemy)
- **Frontend:** HTML + Bootstrap + a bit of vanilla JS
- **Auth:** Session-based login with password hashing
- **Packaging:** PyInstaller single-file binary
- **DevOps:** Docker multi-stage build + helper scripts

---

## Features

### Application features

- User registration and login (email + password)
- Session-based authentication
- Each user sees **only their own tasks**
- Tasks with:
  - title  
  - description  
  - status: `todo`, `doing`, `done`  
  - creation timestamp
- Kanban board layout with 3 columns:
  - **To Do**
  - **Doing**
  - **Done**
- Simple CRUD:
  - Create task
  - Change task status
  - Delete task

### API

- `GET /api/tasks`  
  Returns the authenticated user’s tasks as JSON.

- `POST /api/tasks`  
  Accepts JSON payload:
  ```json
  {
    "title": "My task",
    "des
