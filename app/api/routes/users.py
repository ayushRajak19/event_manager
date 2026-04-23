"""
User routes - User portal and personal management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.core import require_user
from app.models import User
from app.schemas.auth import UserResponse

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/profile", response_model=UserResponse, dependencies=[Depends(require_user)])
async def get_user_profile(
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile.
    
    Returns:
        UserResponse: User profile details
    """
    user_id = current_user["user_id"]
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/profile", response_model=UserResponse, dependencies=[Depends(require_user)])
async def update_user_profile(
    name: str = None,
    phone: str = None,
    current_user: dict = Depends(require_user),
    db: Session = Depends(get_db)
):
    """
    Update user's profile.
    
    Args:
        name: Updated name
        phone: Updated phone
        
    Returns:
        UserResponse: Updated user profile
    """
    user_id = current_user["user_id"]
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if name:
        user.name = name
    if phone is not None:
        user.phone = phone
    
    db.commit()
    db.refresh(user)
    
    return user
