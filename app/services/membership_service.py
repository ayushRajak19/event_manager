"""
Membership service - Business logic for membership management.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.membership import Membership
from app.schemas.membership import MembershipRequest, MembershipExtendRequest
import uuid


class MembershipService:
    """Service for membership operations."""
    
    @staticmethod
    def create_membership(db: Session, membership_data: MembershipRequest) -> Membership:
        """Create a new membership."""
        # Calculate expiry date based on type
        start_date = datetime.utcnow()
        if membership_data.membership_type == "6_months":
            expiry_date = start_date + timedelta(days=180)
        elif membership_data.membership_type == "1_year":
            expiry_date = start_date + timedelta(days=365)
        elif membership_data.membership_type == "2_years":
            expiry_date = start_date + timedelta(days=730)
        else:
            expiry_date = start_date + timedelta(days=180)
        
        # Generate unique membership number
        membership_number = f"MEM-{uuid.uuid4().hex[:12].upper()}"
        
        membership = Membership(
            user_id=membership_data.user_id,
            membership_number=membership_number,
            membership_type=membership_data.membership_type,
            start_date=start_date,
            expiry_date=expiry_date,
            amount_paid=membership_data.amount_paid,
            status="active"
        )
        
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership
    
    @staticmethod
    def get_membership(db: Session, membership_id: int) -> Membership:
        """Get membership by ID."""
        return db.query(Membership).filter(Membership.id == membership_id).first()
    
    @staticmethod
    def get_user_membership(db: Session, user_id: int) -> Membership:
        """Get active membership for a user."""
        return db.query(Membership).filter(
            Membership.user_id == user_id,
            Membership.status == "active"
        ).order_by(Membership.created_at.desc()).first()
    
    @staticmethod
    def get_all_memberships(db: Session, page: int = 1, limit: int = 10) -> tuple:
        """Get all memberships with pagination."""
        skip = (page - 1) * limit
        total = db.query(Membership).count()
        memberships = db.query(Membership).offset(skip).limit(limit).all()
        return memberships, total
    
    @staticmethod
    def extend_membership(db: Session, extend_data: MembershipExtendRequest) -> Membership:
        """Extend an existing membership."""
        membership = db.query(Membership).filter(
            Membership.id == extend_data.membership_id
        ).first()
        
        if not membership:
            return None
        
        # Update expiry date
        old_expiry = membership.expiry_date
        if extend_data.new_type == "6_months":
            new_expiry = old_expiry + timedelta(days=180)
        elif extend_data.new_type == "1_year":
            new_expiry = old_expiry + timedelta(days=365)
        elif extend_data.new_type == "2_years":
            new_expiry = old_expiry + timedelta(days=730)
        else:
            new_expiry = old_expiry + timedelta(days=180)
        
        membership.expiry_date = new_expiry
        membership.membership_type = extend_data.new_type
        membership.amount_paid += extend_data.amount_paid
        membership.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(membership)
        return membership
    
    @staticmethod
    def cancel_membership(db: Session, membership_id: int) -> Membership:
        """Cancel a membership."""
        membership = db.query(Membership).filter(
            Membership.id == membership_id
        ).first()
        
        if membership:
            membership.status = "cancelled"
            membership.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(membership)
        
        return membership
    
    @staticmethod
    def check_expired_memberships(db: Session) -> int:
        """Mark expired memberships as expired."""
        now = datetime.utcnow()
        expired = db.query(Membership).filter(
            Membership.expiry_date <= now,
            Membership.status == "active"
        ).update({"status": "expired"})
        db.commit()
        return expired
