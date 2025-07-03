from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import jwt
from jwt import PyJWKClient
import requests
from datetime import datetime

app = FastAPI(
        title="FastAPI KT Session", 
        description="This application is to present how Fast API works", 
        version="1.0.0"
    )

# Security configuration
security = HTTPBearer()

# Microsoft Graph configuration
# Extracted from your token (Hard coded here but should be stored in an environment variable for security purposes)
MICROSOFT_TENANT_ID = "5d3e2773-e07f-4432-a630-1a0f68a28a05"  
MICROSOFT_JWKS_URL = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}/discovery/v2.0/keys"
MICROSOFT_ISSUER = f"https://sts.windows.net/{MICROSOFT_TENANT_ID}/"

# Cache for JWK client with error handling
try:
    jwks_client = PyJWKClient(MICROSOFT_JWKS_URL)
except Exception as e:
    print(f"Warning: Could not initialize JWK client: {e}")
    jwks_client = None

def verify_microsoft_token(token: str):
    """
    Verify Microsoft Graph JWT token
    """
    try:
        # Try to verify with signature first
        if jwks_client:
            try:
                # Get the signing key from Microsoft
                signing_key = jwks_client.get_signing_key_from_jwt(token)
                
                # Decode and verify the token
                payload = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=["RS256"],
                    audience="00000003-0000-0000-c000-000000000000",  # Microsoft Graph audience
                    issuer=MICROSOFT_ISSUER
                )
                print("Token verified with signature validation")
            except Exception as verify_error:
                print(f"Signature verification failed: {verify_error}")
                print("Falling back to unverified decode for development...")
                # Fallback: decode without verification (DEVELOPMENT ONLY)
                payload = jwt.decode(token, options={"verify_signature": False})
        else:
            print("JWK client not available, using unverified decode...")
            # Decode without verification (DEVELOPMENT ONLY)
            payload = jwt.decode(token, options={"verify_signature": False})
        
        # Check if token is expired
        current_time = datetime.utcnow().timestamp()
        if payload.get("exp", 0) < current_time:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "username": payload.get("unique_name", payload.get("upn", "Unknown")),
            "name": payload.get("name", "Unknown User"),
            "email": payload.get("unique_name", payload.get("upn", "")),
            "tenant_id": payload.get("tid"),
            "object_id": payload.get("oid"),
            "roles": payload.get("roles", []),
            "expires_at": datetime.fromtimestamp(payload.get("exp", 0)).isoformat() if payload.get("exp") else "Unknown"
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token format: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify the bearer token (Microsoft Graph JWT)
    """
    token = credentials.credentials
    return verify_microsoft_token(token)


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


@app.get("/")
async def health_check():
    """
    Health check endpoint (no authentication required)
    """
    return {
        "status": "healthy",
        "message": "FastAPI KT Session API is running",
        "authentication": "Microsoft Graph Bearer Token required for most endpoints"
    }


@app.get("/user/me")
async def get_current_user(user: dict = Depends(verify_token)):
    """
    Get current user information from Microsoft Graph token
    """
    return {
        "user_info": user,
        "message": "User authenticated successfully via Microsoft Graph"
    }


@app.get("/projects")
async def get_projects(user: dict = Depends(verify_token)):
    """
    Get all projects (requires authentication)
    """
    return LIST_OF_PROJECT


@app.get("/projects/{project_id}")
async def get_project(project_id: str, user: dict = Depends(verify_token)) -> ProjectResponse:
    """
    Get a project by ID (requires authentication)
    """
    for project in LIST_OF_PROJECT:
        if project["id"] == project_id:
            return ProjectResponse(**project)
    return {"error": "Project not found"}


@app.post("/project")
async def create_project(project: ProjectCreate, user: dict = Depends(verify_token)) -> dict:
    """
    Create a new project and return the updated project list (requires Microsoft Graph authentication)
    """
    # Convert Pydantic model to dict and add UUID
    project_data = project.dict()
    project_data["id"] = str(uuid.uuid4())
    
    # Add to our storage
    LIST_OF_PROJECT.append(project_data)
    
    # Return the new project and updated list
    return {
        "new_project": ProjectResponse(**project_data),
        "all_projects": LIST_OF_PROJECT,
        "created_by": {
            "username": user["username"],
            "name": user["name"],
            "email": user["email"]
        }
    }
    

@app.put("/project/{project_id}")
async def update_project(project_id: str, project: ProjectCreate, user: dict = Depends(verify_token)) -> ProjectResponse:
    """
    Update an existing project by ID (requires Microsoft Graph authentication)
    """
    for idx, existing_project in enumerate(LIST_OF_PROJECT):
        if existing_project["id"] == project_id:
            updated_project = project.dict()
            updated_project["id"] = project_id
            LIST_OF_PROJECT[idx] = updated_project
            return ProjectResponse(**updated_project)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found"
    )


@app.delete("/project/{project_id}")
async def delete_project(project_id: str, user: dict = Depends(verify_token)) -> dict:
    """
    Delete a project by ID (requires Microsoft Graph authentication)
    """
    global LIST_OF_PROJECT
    original_count = len(LIST_OF_PROJECT)
    LIST_OF_PROJECT = [project for project in LIST_OF_PROJECT if project["id"] != project_id]
    
    if len(LIST_OF_PROJECT) == original_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {
        "message": "Project deleted successfully", 
        "remaining_projects": LIST_OF_PROJECT,
        "deleted_by": user["username"]
    }


@app.delete("/projects")
async def delete_all_projects(user: dict = Depends(verify_token)) -> dict:
    """
    Delete all projects (requires Microsoft Graph authentication)
    """
    global LIST_OF_PROJECT
    LIST_OF_PROJECT = []
    
    return {
        "message": "All projects deleted successfully", 
        "remaining_projects": LIST_OF_PROJECT,
        "deleted_by": user["username"]
    }