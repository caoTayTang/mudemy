from fastapi import FastAPI
from .api import *


def create_app() -> FastAPI:
    """App factory to create FastAPI instance."""
    app = FastAPI(
        title="Mudemy",
        description="Backend service for mudemy.",
        version="1.0.0"
    )

    app.include_router(routes_utils.router, tags=["Utils"])
    app.include_router(routes_login.router, prefix="/api/auth", tags=["Login"])
    app.include_router(routes_user.router, prefix="/api", tags=["User"])
    app.include_router(routes_course.router, prefix="/api", tags=["Course"])
    

    app.include_router(routes_assessment.router, prefix="/api", tags=["Assessment"])
    app.include_router(routes_enrollment.router, prefix="/api", tags=["Enrollment"])
    app.include_router(routes_resource.router, prefix="/api", tags=["Resource"])
    
    return app