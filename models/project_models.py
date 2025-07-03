from pydantic import BaseModel, Field


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


class UserInfo(BaseModel):
    """Model for user information from Microsoft Graph"""
    username: str
    name: str
    email: str
    tenant_id: str
    object_id: str
    roles: list
    expires_at: str
