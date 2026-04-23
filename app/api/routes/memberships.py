"""
Membership routes - API endpoints for membership management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.membership import MembershipRequest, MembershipResponse, MembershipExtendRequest
from app.services.membership_service import MembershipService
from app.core.security import verify_token
from app.core.roles import require_admin, require_user

router = APIRouter(prefix="/memberships", tags=["Memberships"])


@router.post("", response_model=MembershipResponse, dependencies=[Depends(require_admin)])
async def create_membership(
    membership_data: MembershipRequest,
    db: Session = Depends(get_db)
):
    """Create a new membership (Admin only)."""
    try:
        membership = MembershipService.create_membership(db, membership_data)
        return membership
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create membership: {str(e)}"
        )


@router.get("/{membership_id}", response_model=MembershipResponse, dependencies=[Depends(require_admin)])
async def get_membership(
    membership_id: int,
    db: Session = Depends(get_db)
):
    """Get membership details by ID."""
    membership = MembershipService.get_membership(db, membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    return membership


@router.get("/user/{user_id}", response_model=MembershipResponse)
async def get_user_membership(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """Get active membership for a user."""
    # User can only see their own membership, admin can see any
    if current_user["role"] != "admin" and current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this membership"
        )
    
    membership = MembershipService.get_user_membership(db, user_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active membership found"
        )
    return membership


@router.get("", dependencies=[Depends(require_admin)])
async def get_all_memberships(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all memberships with pagination (Admin only)."""
    memberships, total = MembershipService.get_all_memberships(db, page, limit)
    return {
        "total": total,
        "count": len(memberships),
        "page": page,
        "limit": limit,
        "memberships": memberships
    }


@router.put("/{membership_id}", response_model=MembershipResponse, dependencies=[Depends(require_admin)])
async def extend_membership(
    membership_id: int,
    extend_data: MembershipExtendRequest,
    db: Session = Depends(get_db)
):
    """Extend an existing membership (Admin only)."""
    extend_data.membership_id = membership_id
    membership = MembershipService.extend_membership(db, extend_data)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    return membership


@router.delete("/{membership_id}", dependencies=[Depends(require_admin)])
async def cancel_membership(
    membership_id: int,
    db: Session = Depends(get_db)
):
    """Cancel a membership (Admin only)."""
    membership = MembershipService.cancel_membership(db, membership_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    return {"message": "Membership cancelled successfully", "membership": membership}


@router.post("/check-expired", dependencies=[Depends(require_admin)])
async def check_expired_memberships(
    db: Session = Depends(get_db)
):
    """Check and update expired memberships (Admin only)."""
    count = MembershipService.check_expired_memberships(db)
    return {"message": f"Updated {count} expired memberships"}
