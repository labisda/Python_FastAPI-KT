from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
import uuid

app = FastAPI(
        title="FastAPI KT Session", 
        description="This application is to present how Fast API works", 
        version="1.0.0"
    )


# Pydantic models for request/response validation
class ProjectBase(BaseModel):
    name: str = Field(..., description="The name of the project", min_length=1, max_length=100)
    description: str = Field(..., description="The description of the project", min_length=1, max_length=500)
    status: str = Field(..., description="The status of the project", pattern="^(Not Started|In Progress|Complete|Completed)$")


class ProjectCreate(ProjectBase):
    """Model for creating a new project"""
    pass


class ProjectResponse(ProjectBase):
    """Model for project response with ID"""
    id: str = Field(..., description="The unique identifier of the project")


# Set local variable as the storage of data
LIST_OF_PROJECT = [
    {
        "id": '123e4567-e89b-12d3-a456-426614174123',
        "name": "iCoach",
        "description": "This is a project for iCoach",
        "status": "Complete"
    }
]


@app.get("/projects")
async def get_projects():
    """
    Get all projects
    """
    return LIST_OF_PROJECT


@app.get("/projects/{project_id}")
async def get_project(project_id: str) -> ProjectResponse:
    """
    Get a project by ID
    """
    for project in LIST_OF_PROJECT:
        if project["id"] == project_id:
            return ProjectResponse(**project)
    return {"error": "Project not found"}


@app.post("/project")
async def create_project(project: ProjectCreate) -> dict:
    """
    Create a new project and return the updated project list
    """
    # Convert Pydantic model to dict and add UUID
    project_data = project.dict()
    project_data["id"] = str(uuid.uuid4())
    
    # Add to our storage
    LIST_OF_PROJECT.append(project_data)
    
    # Return the new project and updated list
    return {
        "new_project": ProjectResponse(**project_data),
        "all_projects": LIST_OF_PROJECT
    }
    

@app.put("/project/{project_id}")
async def update_project(project_id: str, project: ProjectCreate) -> ProjectResponse:
    """
    Update an existing project by ID
    """
    for idx, existing_project in enumerate(LIST_OF_PROJECT):
        if existing_project["id"] == project_id:
            updated_project = project.dict()
            updated_project["id"] = project_id
            LIST_OF_PROJECT[idx] = updated_project
            return ProjectResponse(**updated_project)
    
    return {"error": "Project not found"}


@app.delete("/project/{project_id}")
async def delete_project(project_id: str) -> dict:
    """
    Delete a project by ID
    """
    global LIST_OF_PROJECT
    LIST_OF_PROJECT = [project for project in LIST_OF_PROJECT if project["id"] != project_id]
    
    return {"message": "Project deleted successfully", "remaining_projects": LIST_OF_PROJECT}


@app.delete("/projects")
async def delete_all_projects() -> dict:
    """
    Delete all projects
    """
    global LIST_OF_PROJECT
    LIST_OF_PROJECT = []
    
    return {"message": "All projects deleted successfully", "remaining_projects": LIST_OF_PROJECT}