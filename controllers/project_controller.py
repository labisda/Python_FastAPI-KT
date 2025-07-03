from fastapi import HTTPException, status
from typing import List, Dict, Optional
import uuid
from models.project_models import ProjectCreate, ProjectResponse

# Set local variable as the storage of data
LIST_OF_PROJECT = [
    {
        "id": '123e4567-e89b-12d3-a456-426614174123',
        "name": "iCoach",
        "description": "This is a project for iCoach",
        "status": "Complete"
    }
]


class ProjectController:
    """Controller for project-related business logic"""
    
    @staticmethod
    def get_all_projects() -> List[Dict]:
        """Get all projects"""
        return LIST_OF_PROJECT
    
    @staticmethod
    def get_project_by_id(project_id: str) -> Optional[Dict]:
        """Get a project by ID"""
        for project in LIST_OF_PROJECT:
            if project["id"] == project_id:
                return project
        return None
    
    @staticmethod
    def create_project(project_data: ProjectCreate) -> Dict:
        """Create a new project"""
        # Convert Pydantic model to dict and add UUID
        project_dict = project_data.dict()
        project_dict["id"] = str(uuid.uuid4())
        
        # Add to our storage
        LIST_OF_PROJECT.append(project_dict)
        
        return project_dict
    
    @staticmethod
    def update_project(project_id: str, project_data: ProjectCreate) -> Optional[Dict]:
        """Update an existing project"""
        for idx, existing_project in enumerate(LIST_OF_PROJECT):
            if existing_project["id"] == project_id:
                updated_project = project_data.dict()
                updated_project["id"] = project_id
                LIST_OF_PROJECT[idx] = updated_project
                return updated_project
        return None
    
    @staticmethod
    def delete_project(project_id: str) -> bool:
        """Delete a project by ID"""
        global LIST_OF_PROJECT
        original_count = len(LIST_OF_PROJECT)
        LIST_OF_PROJECT = [project for project in LIST_OF_PROJECT if project["id"] != project_id]
        return len(LIST_OF_PROJECT) < original_count
    
    @staticmethod
    def delete_all_projects() -> None:
        """Delete all projects"""
        global LIST_OF_PROJECT
        LIST_OF_PROJECT = []
