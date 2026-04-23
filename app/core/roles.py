"""
Role-based access control decorators and utilities.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional
from app.core.security import verify_token
from app.db import get_db
from app.models.enums import UserRole


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Dependency to get current authenticated user.
    
    Extracts user info from JWT token in Authorization header.
    
    Args:
        credentials: HTTP Bearer credentials from request
        db: Database session
        
    Returns:
        dict: Token payload with user information
        
    Raises:
        HTTPException: If token is invalid, expired, or missing
    """
    token = credentials.credentials
    
    try:
        payload = verify_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    role = payload.get("role")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": int(user_id),
        "role": role,
        "email": payload.get("email"),
        "token": token
    }


async def require_role(required_role: UserRole):
    """
    Dependency factory for role-based authorization.
    
    Creates a dependency that checks if current user has required role.
    
    Args:
        required_role: Required user role
        
    Returns:
        Callable: Dependency function
        
    Example:
        @app.post("/admin/users/")
        async def create_user(
            user_data: UserCreate,
            current_user = Depends(get_current_user),
            authorized = Depends(require_role(UserRole.ADMIN))
        ):
            # This endpoint only works for admin users
            pass
    """
    async def check_role(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        
        if user_role != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires {required_role.value} role"
            )
        
        return current_user
    
    return check_role


# Convenience dependencies for common roles
async def require_admin(current_user: dict = Depends(get_current_user)):
    """Dependency to require admin role."""
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_vendor(current_user: dict = Depends(get_current_user)):
    """Dependency to require vendor role."""
    if current_user.get("role") != UserRole.VENDOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vendor access required"
        )
    return current_user


async def require_user(current_user: dict = Depends(get_current_user)):
    """Dependency to require regular user role."""
    if current_user.get("role") != UserRole.USER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User access required"
        )
    return current_user
