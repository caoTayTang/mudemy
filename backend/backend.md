# Backend Folder Structure

This document explains the backend folder structure of the MuTor project. The backend is built using **FastAPI** and **SQLAlchemy**.

```

./backend

```
Contains the entire backend project.

---

## **Main Folders and Files**

### 1. `app/`
Contains the core backend logic.

#### **Subfolders**
- `api/` – Defines API endpoints (routers):
  - `courses.py` – Handles `/courses` related routes (list, enroll, create, etc.).
  - `notifications.py` – Handles `/notifications` routes.
  - `__init__.py` – Initializes the API package.
- `services/` – Business logic and interaction with models:
  - `course_service.py` – Core logic for course operations.
  - `__init__.py` – Initializes the services package.
- `models/` – Database models (tables) using SQLAlchemy:
  - `course.py` – Course table definition.
  - `notification.py` – Notification table definition.
- `database/` – Database connection and session management:
  - `__init__.py` – Initializes the database package.
- `core/` – Core configuration:
  - `config.py` – App settings (e.g., database URL).
  - `__init__.py` – Initializes the core package.
- `tests/` – Unit tests for backend:
  - `__init__.py` – Test package initialization.

---

### 2. Root Files
- `main.py` – Entry point; initializes FastAPI app and includes routers.
- `__pycache__/` – Python cache files (auto-generated).

---

### **Summary**
- `api` → Route definitions, exposed to frontend.
- `services` → Business logic, communicates with models and database.
- `models` → Database table definitions.
- `database` → Session and connection management.
- `core` → Configuration and app settings.
- `tests` → Unit tests.

---

### **CORS Setup**
Frontend React app runs on `localhost:3000`, backend FastAPI on `localhost:8000`. CORS middleware is configured to allow frontend requests.