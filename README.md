# FastAPI Folders & Files Structure

## Prerequisite
- Python ([Download here](https://www.python.org/downloads/))

## Project Structure

```
FastAPI-KT-App/
├── app.py                          # Main FastAPI application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── __pycache__/                    # Python cache files
├── models/                         # Pydantic models and data structures
│   ├── __init__.py                 # Package marker
│   └── project_models.py           # Project-related models (ProjectBase, ProjectCreate, ProjectResponse, UserInfo)
├── routes/                         # API endpoint definitions
│   ├── __init__.py                 # Package marker
│   ├── project_routes.py           # Project CRUD endpoints (/api/v1/projects)
│   └── auth_routes.py              # Authentication & health check endpoints (/api/v1/auth, /)
├── authentication/                 # Authentication logic
│   ├── __init__.py                 # Package marker
│   └── auth.py                     # Microsoft Graph JWT token verification
└── controllers/                    # Business logic layer
    ├── __init__.py                 # Package marker
    └── project_controller.py       # Project business logic and data operations
```

## API Endpoints

### Health Check
- `GET /` - Health check endpoint (no authentication required)

### Authentication
- `GET /api/v1/auth/me` - Get current user information from Microsoft Graph token

### Projects
- `GET /api/v1/projects/` - Get all projects
- `GET /api/v1/projects/{project_id}` - Get project by ID
- `POST /api/v1/projects/` - Create new project
- `PUT /api/v1/projects/{project_id}` - Update existing project
- `DELETE /api/v1/projects/{project_id}` - Delete specific project
- `DELETE /api/v1/projects/` - Delete all projects

## Features

- **Microsoft Graph Authentication**: JWT token verification with fallback for development
- **Organized Architecture**: Separation of concerns with models, routes, controllers, and authentication
- **API Versioning**: All endpoints use `/api/v1/` prefix
- **Interactive Documentation**: Auto-generated Swagger UI available at `/docs`
- **Type Safety**: Full Pydantic model validation for request/response data

## How to run locally

1. Clone the repository
```
git clone https://github.com/labisda/Python_FastAPI-KT.git
```

2. Locate the repository via terminal
```
cd Document/Github/Python_FastAPI-KT
```

3. Create a virtual environment
```
python -m venv venv
```

4. Run the virtual environment
```
venv\Scripts\activate
```

5. Install required libraries
```
pip install -r requirements.txt
```

6. Once installed, run the server using uvicorn
```
uvicorn app:app --reload
```

## References

### Technologies Used

<div align="center">

| Technology | Description | Documentation |
|------------|-------------|---------------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | High-level programming language | [Python Official Docs](https://docs.python.org/) |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | Modern, fast web framework for building APIs | [FastAPI Documentation](https://fastapi.tiangolo.com/) |
| ![Microsoft Graph](https://img.shields.io/badge/Microsoft%20Graph-0078D4?style=for-the-badge&logo=microsoft&logoColor=white) | API gateway to Microsoft 365 services | [Microsoft Graph Docs](https://docs.microsoft.com/en-us/graph/) |

</div>

### Additional Resources

- **FastAPI Tutorial**: [Getting Started Guide](https://fastapi.tiangolo.com/tutorial/)
- **Python JWT**: [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- **Microsoft Graph Authentication**: [Auth Overview](https://docs.microsoft.com/en-us/graph/auth/)
- **Pydantic Models**: [Data Validation](https://pydantic-docs.helpmanual.io/)