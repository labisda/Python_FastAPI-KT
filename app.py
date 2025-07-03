from fastapi import FastAPI
from routes.project_routes import router as project_router
from routes.auth_routes import health_router, auth_router

app = FastAPI(
        title="FastAPI KT Session", 
        description="This application is to present how Fast API works", 
        version="1.0.0"
    )

# Include routers with proper organization
app.include_router(health_router)           # Health check at root
app.include_router(auth_router)             # Authentication endpoints
app.include_router(project_router)          # Project management endpoints