from fastapi import APIRouter, Depends, HTTPException, status
from models.project_models import ProjectCreate, ProjectResponse
from authentication.auth import verify_token
from controllers.project_controller import ProjectController

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_projects(user: dict = Depends(verify_token)):
    """
    Get all projects (requires authentication)
    """
    return ProjectController.get_all_projects()


@router.get("/{project_id}")
async def get_project(project_id: str, user: dict = Depends(verify_token)) -> ProjectResponse:
    """
    Get a project by ID (requires authentication)
    """
    project = ProjectController.get_project_by_id(project_id)
    if project:
        return ProjectResponse(**project)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found"
    )


@router.post("/")
async def create_project(project: ProjectCreate, user: dict = Depends(verify_token)) -> dict:
    """
    Create a new project and return the updated project list (requires Microsoft Graph authentication)
    """
    new_project = ProjectController.create_project(project)
    
    # Return the new project and updated list
    return {
        "new_project": ProjectResponse(**new_project),
        "all_projects": ProjectController.get_all_projects(),
        "created_by": {
            "username": user["username"],
            "name": user["name"],
            "email": user["email"]
        }
    }


@router.put("/{project_id}")
async def update_project(project_id: str, project: ProjectCreate, user: dict = Depends(verify_token)) -> ProjectResponse:
    """
    Update an existing project by ID (requires Microsoft Graph authentication)
    """
    updated_project = ProjectController.update_project(project_id, project)
    if updated_project:
        return ProjectResponse(**updated_project)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found"
    )


@router.delete("/{project_id}")
async def delete_project(project_id: str, user: dict = Depends(verify_token)) -> dict:
    """
    Delete a project by ID (requires Microsoft Graph authentication)
    """
    deleted = ProjectController.delete_project(project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {
        "message": "Project deleted successfully", 
        "remaining_projects": ProjectController.get_all_projects(),
        "deleted_by": user["username"]
    }


@router.delete("/")
async def delete_all_projects(user: dict = Depends(verify_token)) -> dict:
    """
    Delete all projects (requires Microsoft Graph authentication)
    """
    ProjectController.delete_all_projects()
    
    return {
        "message": "All projects deleted successfully", 
        "remaining_projects": ProjectController.get_all_projects(),
        "deleted_by": user["username"]
    }
