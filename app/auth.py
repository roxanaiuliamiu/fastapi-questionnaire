from fastapi import HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# User credentials
USERS = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

# Admin password
ADMIN_PASSWORD = "4dm1N"

def verify_user(credentials: HTTPBasicCredentials = Security(security)) -> str:
    """
    Verify user credentials for regular endpoints.
    Returns username if valid, raises HTTPException if invalid.
    """
    username = credentials.username
    password = credentials.password
    
    # Check if user exists and password matches
    if username in USERS and USERS[username] == password:
        return username
    
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

def verify_admin(credentials: HTTPBasicCredentials = Security(security)) -> bool:
    """
    Verify admin credentials for admin-only endpoints.
    Returns True if valid admin, raises HTTPException if invalid.
    """
    password = credentials.password
    
    # Check if password matches admin password
    if password == ADMIN_PASSWORD:
        return True
    
    raise HTTPException(
        status_code=401,
        detail="Admin authentication required",
        headers={"WWW-Authenticate": "Basic"},
    )