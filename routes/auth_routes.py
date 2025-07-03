from fastapi import APIRouter, Depends
from authentication.auth import verify_token

# Health check router (no prefix)
health_router = APIRouter(
    tags=["Health Check"]
)

# Authentication router
auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
    responses={401: {"description": "Unauthorized"}},
)


@health_router.get("/")
async def health_check():
    """
    Health check endpoint (no authentication required)
    """
    return {
        "status": "healthy",
        "message": "FastAPI KT Session API is running",
        "authentication": "Microsoft Graph Bearer Token required for most endpoints"
    }


@auth_router.get("/me")
async def get_current_user(user: dict = Depends(verify_token)):
    """
    Get current user information from Microsoft Graph token
    """
    return {
        "user_info": user,
        "message": "User authenticated successfully via Microsoft Graph"
    }
