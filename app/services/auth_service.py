"""
Authentication service - User registration and login logic.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import timedelta
from app.models import Admin, User, Vendor
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import (
    AdminSignup, UserSignup, TokenResponse
)
from app.config import settings


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def admin_signup(db: Session, signup_data: AdminSignup) -> TokenResponse:
        """
        Register a new admin user.
        
        Args:
            db: Database session
            signup_data: Admin signup information
            
        Returns:
            TokenResponse: Access token and user info
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if admin with this email already exists
        existing_admin = db.query(Admin).filter(Admin.email == signup_data.email).first()
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new admin
        hashed_password = hash_password(signup_data.password)
        new_admin = Admin(
            name=signup_data.name,
            email=signup_data.email,
            password_hash=hashed_password
        )

        try:
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create access token
        access_token = create_access_token(
            data={"sub": str(new_admin.id), "role": "admin", "email": new_admin.email}
        )

        return TokenResponse(
            access_token=access_token,
            user_id=new_admin.id,
            email=new_admin.email,
            name=new_admin.name,
            role="admin"
        )

    @staticmethod
    def admin_login(db: Session, email: str, password: str) -> TokenResponse:
        """
        Authenticate admin user.
        
        Args:
            db: Database session
            email: Admin email
            password: Admin password
            
        Returns:
            TokenResponse: Access token and user info
            
        Raises:
            HTTPException: If credentials are invalid
        """
        admin = db.query(Admin).filter(Admin.email == email).first()
        
        if not admin or not verify_password(password, admin.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            data={"sub": str(admin.id), "role": "admin", "email": admin.email}
        )

        return TokenResponse(
            access_token=access_token,
            user_id=admin.id,
            email=admin.email,
            name=admin.name,
            role="admin"
        )

    @staticmethod
    def user_signup(db: Session, signup_data: UserSignup) -> TokenResponse:
        """
        Register a new user.
        
        Args:
            db: Database session
            signup_data: User signup information
            
        Returns:
            TokenResponse: Access token and user info
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user with this email already exists
        existing_user = db.query(User).filter(User.email == signup_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = hash_password(signup_data.password)
        new_user = User(
            name=signup_data.name,
            email=signup_data.email,
            password_hash=hashed_password,
            phone=signup_data.phone
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create access token
        access_token = create_access_token(
            data={"sub": str(new_user.id), "role": "user", "email": new_user.email}
        )

        return TokenResponse(
            access_token=access_token,
            user_id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            role="user"
        )

    @staticmethod
    def user_login(db: Session, email: str, password: str) -> TokenResponse:
        """
        Authenticate user.
        
        Args:
            db: Database session
            email: User email
            password: User password
            
        Returns:
            TokenResponse: Access token and user info
            
        Raises:
            HTTPException: If credentials are invalid
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        access_token = create_access_token(
            data={"sub": str(user.id), "role": "user", "email": user.email}
        )

        return TokenResponse(
            access_token=access_token,
            user_id=user.id,
            email=user.email,
            name=user.name,
            role="user"
        )

    @staticmethod
    def vendor_login(db: Session, email: str, password: str) -> TokenResponse:
        """
        Authenticate vendor.
        
        Args:
            db: Database session
            email: Vendor email
            password: Vendor password
            
        Returns:
            TokenResponse: Access token and vendor info
            
        Raises:
            HTTPException: If credentials are invalid or vendor is inactive
        """
        vendor = db.query(Vendor).filter(Vendor.email == email).first()
        
        if not vendor or not verify_password(password, vendor.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if vendor.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vendor account is not active"
            )

        access_token = create_access_token(
            data={"sub": str(vendor.id), "role": "vendor", "email": vendor.email}
        )

        return TokenResponse(
            access_token=access_token,
            user_id=vendor.id,
            email=vendor.email,
            name=vendor.name,
            role="vendor"
        )
