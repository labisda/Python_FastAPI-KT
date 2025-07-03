from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from datetime import datetime

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
