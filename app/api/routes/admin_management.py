"""
Admin management routes - Additional admin features.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.roles import require_admin
from app.models import User, Order, Vendor, Membership, Transaction
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin-management", tags=["Admin Management"])


@router.get("/maintenance/status", dependencies=[Depends(require_admin)])
async def get_maintenance_status(db: Session = Depends(get_db)):
    """Get system maintenance status and health."""
    try:
        total_users = db.query(User).count()
        total_vendors = db.query(Vendor).count()
        total_orders = db.query(Order).count()
        total_memberships = db.query(Membership).count()
        
        # Last 24 hours stats
        yesterday = datetime.utcnow() - timedelta(days=1)
        new_users = db.query(User).filter(User.created_at >= yesterday).count()
        new_orders = db.query(Order).filter(Order.created_at >= yesterday).count()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "database": "connected",
            "total_users": total_users,
            "total_vendors": total_vendors,
            "total_orders": total_orders,
            "total_memberships": total_memberships,
            "new_users_24h": new_users,
            "new_orders_24h": new_orders
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Maintenance check failed: {str(e)}"
        )


@router.get("/reports/dashboard", dependencies=[Depends(require_admin)])
async def get_dashboard_report(db: Session = Depends(get_db)):
    """Get comprehensive dashboard report."""
    try:
        # User stats
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == 1).count()
        
        # Vendor stats
        total_vendors = db.query(Vendor).count()
        active_vendors = db.query(Vendor).filter(Vendor.is_active == 1).count()
        
        # Order stats
        total_orders = db.query(Order).count()
        pending_orders = db.query(Order).filter(Order.status == "pending").count()
        completed_orders = db.query(Order).filter(Order.status == "delivered").count()
        
        # Membership stats
        active_memberships = db.query(Membership).filter(Membership.status == "active").count()
        expired_memberships = db.query(Membership).filter(Membership.status == "expired").count()
        
        # Transaction stats
        total_transactions = db.query(Transaction).count()
        total_revenue = sum([t.amount for t in db.query(Transaction).all()]) if total_transactions > 0 else 0
        
        return {
            "users": {
                "total": total_users,
                "active": active_users,
                "inactive": total_users - active_users
            },
            "vendors": {
                "total": total_vendors,
                "active": active_vendors,
                "inactive": total_vendors - active_vendors
            },
            "orders": {
                "total": total_orders,
                "pending": pending_orders,
                "completed": completed_orders
            },
            "memberships": {
                "active": active_memberships,
                "expired": expired_memberships
            },
            "transactions": {
                "total": total_transactions,
                "total_revenue": total_revenue
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )


@router.get("/reports/members-transaction", dependencies=[Depends(require_admin)])
async def get_members_transaction_report(db: Session = Depends(get_db)):
    """Get membership and transaction reports."""
    try:
        # Membership types breakdown
        memberships = db.query(Membership).all()
        type_breakdown = {
            "6_months": len([m for m in memberships if m.membership_type == "6_months"]),
            "1_year": len([m for m in memberships if m.membership_type == "1_year"]),
            "2_years": len([m for m in memberships if m.membership_type == "2_years"])
        }
        
        # Transaction breakdown
        transactions = db.query(Transaction).all()
        transaction_breakdown = {
            "membership_purchase": len([t for t in transactions if t.transaction_type == "membership_purchase"]),
            "order_payment": len([t for t in transactions if t.transaction_type == "order_payment"]),
            "refund": len([t for t in transactions if t.transaction_type == "refund"])
        }
        
        # Revenue by month (last 3 months)
        three_months_ago = datetime.utcnow() - timedelta(days=90)
        recent_transactions = db.query(Transaction).filter(
            Transaction.created_at >= three_months_ago
        ).all()
        
        return {
            "memberships": {
                "total": len(memberships),
                "by_type": type_breakdown,
                "active": len([m for m in memberships if m.status == "active"]),
                "expired": len([m for m in memberships if m.status == "expired"])
            },
            "transactions": {
                "total": len(transactions),
                "by_type": transaction_breakdown,
                "total_revenue": sum([t.amount for t in transactions])
            },
            "recent_revenue_count": len(recent_transactions)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )
