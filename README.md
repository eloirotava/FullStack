# Mini Kanban – Full Stack Flask Demo

A small full stack project that demonstrates how I orchestrate backend, database, frontend, packaging, and Docker in a clean, production-like workflow.

This repo contains a simple Kanban-style task manager built with:

- Backend: Flask (Python)
- Database: SQLite (via SQLAlchemy)
- Frontend: HTML + Bootstrap + a bit of vanilla JS
- Auth: Session-based login with password hashing
- Packaging: PyInstaller single-file binary
- DevOps: Docker multi-stage build + helper scripts

---

## Features

### Application features

- User registration and login (email + password)
- Session-based authentication
- Each user sees only their own tasks
- Tasks with:
  - title
  - description
  - status: todo, doing, done
  - creation timestamp
- Kanban board layout with 3 columns:
  - To Do
  - Doing
  - Done
- Simple CRUD:
  - Create task
  - Change task status
  - Delete task

### API

- GET /api/tasks
  - Returns the authenticated user’s tasks as JSON.

- POST /api/tasks
  - Accepts JSON payload like:
    { "title": "My task", "description": "Optional", "status": "todo" }
  - Creates a task for the current user and returns a small JSON response with the new task id.

The frontend includes a small JS snippet that calls /api/tasks and displays the JSON response, just to show client-side integration with the API.

---

## Tech Stack

- Language: Python 3
- Web framework: Flask
- ORM: Flask-SQLAlchemy (SQLAlchemy 2.x)
- Database: SQLite (file-based)
- Frontend: Bootstrap 5, Jinja2 templates, vanilla JS
- Auth: werkzeug.security password hashing + Flask sessions
- Packaging: PyInstaller (single-file executable)
- Containerization: Docker (multi-stage build)
- Dev tooling:
  - run_dev.sh – development helper (venv + dependencies + run app)
  - build_exe.sh – build single-file executable inside Docker and extract it

---

## Project Structure

High-level layout:

- app.py – Flask application, models, routes (HTML + API), auth
- requirements.txt – Python dependencies
- Dockerfile.pyinstaller – multi-stage Dockerfile used to build the executable image
- run_dev.sh – one-command dev setup and server runner
- build_exe.sh – builds the app into a single executable using Docker + PyInstaller
- .gitignore – ignores venv, build artefacts, instance data, etc.
- templates/
  - base.html
  - index.html
  - login.html
  - register.html
- static/
  - css/custom.css
  - js/main.js

---

## Getting Started (Development)

### Prerequisites

- Python 3.12+
- pip
- (Optional but recommended) virtualenv support
- Docker (for building the binary / container, optional for dev)

### 1. Clone the repository

Clone and enter the project folder:

- git clone https://github.com/<your-username>/<your-repo>.git
- cd <your-repo>

### 2. Run in development mode

There is a helper script that creates a virtualenv, installs dependencies and starts the app:

- ./run_dev.sh

What it does:

1. Creates .venv/ if it does not exist
2. Activates the virtual environment
3. Installs or updates dependencies from requirements.txt
4. Runs python app.py

The app will start on:

- http://127.0.0.1:5000

### 3. First use

1. Open the app in your browser
2. Click “Register” to create an account (any email + password, no email verification)
3. Login with that account
4. Add tasks and move them between To Do / Doing / Done

Each user has its own tasks; they are isolated in the database.

---

## Building a Single-File Executable (PyInstaller + Docker)

To demonstrate packaging and a more DevOps-like workflow, the project includes:

- Dockerfile.pyinstaller
- build_exe.sh

The executable is built inside Docker, so you don’t need PyInstaller or system build tools installed on your host.

### Requirements

- Docker installed and running

### Build the executable (amd64)

From the project root:

- ./build_exe.sh

This script will:

1. Build a Docker image using Dockerfile.pyinstaller
2. Run PyInstaller inside the build stage to generate a single-file binary
3. Extract the binary from the container into the local dist/ folder

When it finishes, you should have:

- dist/kanban-amd64

### Run the executable

On a compatible Linux host:

- ./dist/kanban-amd64

The app will start just like in dev mode, listening on port 5000.

---

## Running via Docker (Containerized App)

You can also use the Docker image that build_exe.sh creates.

If you want to build and run manually:

- docker build -f Dockerfile.pyinstaller -t kanban-pyinstaller-amd64 .
- docker run --rm -p 5000:5000 kanban-pyinstaller-amd64

Then open:

- http://127.0.0.1:5000

---

## Why this project?

This project is intentionally small, but it shows a complete full stack flow:

- Backend: Flask app with routing, templates, JSON API
- Database: SQLAlchemy models and automatic table creation on startup
- Frontend: Bootstrap UI + Kanban board + basic client-side JS using fetch
- Authentication: Session-based login, password hashing
- Developer experience: One-command dev environment (./run_dev.sh)
- Packaging and DevOps:
  - Single-file executable built with PyInstaller inside Docker
  - Multi-stage Dockerfile for clean runtime images
  - Scripted build/extract workflow (./build_exe.sh)

It’s a compact example of how I think about and orchestrate the full development lifecycle: from local development, to packaging, to containerization.
