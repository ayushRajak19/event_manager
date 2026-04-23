"""
Transactions routes - API endpoints for transaction management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.transaction import TransactionRequest, TransactionResponse, TransactionListResponse
from app.services.transaction_service import TransactionService
from app.core.security import verify_token
from app.core.roles import require_admin, require_user
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("", response_model=TransactionResponse, dependencies=[Depends(require_user)])
async def create_transaction(
    transaction_data: TransactionRequest,
    db: Session = Depends(get_db)
):
    """Create a new transaction."""
    try:
        transaction = TransactionService.create_transaction(db, transaction_data)
        return transaction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create transaction: {str(e)}"
        )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """Get transaction details."""
    transaction = TransactionService.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # User can only see their own transactions, admin can see any
    if current_user["role"] != "admin" and transaction.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this transaction"
        )
    
    return transaction


@router.get("/user/all", dependencies=[Depends(require_user)])
async def get_user_transactions(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    """Get all transactions for current user."""
    transactions, total = TransactionService.get_user_transactions(
        db, current_user["user_id"], page, limit
    )
    return {
        "total": total,
        "count": len(transactions),
        "page": page,
        "limit": limit,
        "transactions": transactions
    }


@router.get("", dependencies=[Depends(require_admin)])
async def get_all_transactions(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all transactions (Admin only)."""
    transactions, total = TransactionService.get_all_transactions(db, page, limit)
    return {
        "total": total,
        "count": len(transactions),
        "page": page,
        "limit": limit,
        "transactions": transactions
    }


@router.get("/type/{transaction_type}", dependencies=[Depends(require_admin)])
async def get_transactions_by_type(
    transaction_type: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get transactions by type (Admin only)."""
    transactions, total = TransactionService.get_transactions_by_type(
        db, transaction_type, page, limit
    )
    return {
        "total": total,
        "count": len(transactions),
        "page": page,
        "limit": limit,
        "transactions": transactions
    }


@router.get("/report/summary", dependencies=[Depends(require_admin)])
async def get_report_summary(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """Get transaction report summary (Admin only)."""
    try:
        start = datetime.fromisoformat(start_date) if start_date else None
        end = datetime.fromisoformat(end_date) if end_date else None
        summary = TransactionService.get_report_summary(db, start, end)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate report: {str(e)}"
        )
