"""
Authentication routes - Sign up and login endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.auth import (
    AdminSignup, AdminLogin, UserSignup, UserLogin, VendorLogin, TokenResponse
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/admin/signup", response_model=TokenResponse)
async def admin_signup(
    signup_data: AdminSignup,
    db: Session = Depends(get_db)
):
    """
    Admin signup endpoint.
    
    Creates a new admin account and returns access token.
    
    Args:
        signup_data: Admin registration details
        db: Database session
        
    Returns:
        TokenResponse: Access token and user info
    """
    return AuthService.admin_signup(db, signup_data)


@router.post("/admin/login", response_model=TokenResponse)
async def admin_login(
    login_data: AdminLogin,
    db: Session = Depends(get_db)
):
    """
    Admin login endpoint.
    
    Authenticates admin and returns access token.
    
    Args:
        login_data: Admin credentials
        db: Database session
        
    Returns:
        TokenResponse: Access token and user info
    """
    return AuthService.admin_login(db, login_data.email, login_data.password)


@router.post("/user/signup", response_model=TokenResponse)
async def user_signup(
    signup_data: UserSignup,
    db: Session = Depends(get_db)
):
    """
    User signup endpoint.
    
    Creates a new user account and returns access token.
    
    Args:
        signup_data: User registration details
        db: Database session
        
    Returns:
        TokenResponse: Access token and user info
    """
    return AuthService.user_signup(db, signup_data)


@router.post("/user/login", response_model=TokenResponse)
async def user_login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    User login endpoint.
    
    Authenticates user and returns access token.
    
    Args:
        login_data: User credentials
        db: Database session
        
    Returns:
        TokenResponse: Access token and user info
    """
    return AuthService.user_login(db, login_data.email, login_data.password)


@router.post("/vendor/login", response_model=TokenResponse)
async def vendor_login(
    login_data: VendorLogin,
    db: Session = Depends(get_db)
):
    """
    Vendor login endpoint.
    
    Authenticates vendor and returns access token.
    
    Args:
        login_data: Vendor credentials
        db: Database session
        
    Returns:
        TokenResponse: Access token and vendor info
    """
    return AuthService.vendor_login(db, login_data.email, login_data.password)
