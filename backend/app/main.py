from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
import os
from app import create_app
from app.models import clear_all_sessions

origins = [
    "http://localhost:3000",  # React dev server
]

app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    #http://127.0.0.1:8000/docs   
    #reload_flag = os.getenv("DEBUG", "false").lower() == "true"
    clear_all_sessions()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
