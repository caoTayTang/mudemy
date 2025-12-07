# MUDemy - E-Learning System

## About

**MUDemy** is an E-Learning platform developed by students at the Ho Chi Minh City University of Technology (HCMUT) for the Database Systems course CO2013 - CO2014. The system is designed to manage online education workflows, including course creation, student enrollment, payments, and progress tracking.

The application follows an **MVC (Model-View-Controller)** architecture to ensure separation of concerns:

  * **Backend:** Built with **Python (FastAPI)**, acting as the Application Server to handle business logic and API requests.
  * **Database:** Uses **Microsoft SQL Server** for data storage, utilizing Stored Procedures, Functions, and Triggers to handle complex logic (e.g., auto-generating IDs like `USR00001` and calculating completion rates).
  * **Frontend:** A web-based interface allowing users (Students/Instructors) to interact with courses, quizzes, and assignments.

## How to Run

### 1\. Backend Setup

Navigate to the backend directory, install dependencies, and start the FastAPI server. You should setup the Virtual Environment to avoid packages conflict.

```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

### 2\. Frontend Setup

Open a new terminal shell, navigate to the frontend directory, install dependencies, and launch the development server.

```bash
cd frontend/MUDemy-Frontend/
npm install
npm run dev
```

## Demo video:

```TODO!```

## Report

```TODO!```