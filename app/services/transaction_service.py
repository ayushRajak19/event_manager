"""
Transaction service - Business logic for transaction management.
"""
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionRequest
from datetime import datetime


class TransactionService:
    """Service for transaction operations."""
    
    @staticmethod
    def create_transaction(db: Session, transaction_data: TransactionRequest) -> Transaction:
        """Create a new transaction."""
        transaction = Transaction(
            user_id=transaction_data.user_id,
            transaction_type=transaction_data.transaction_type,
            related_id=transaction_data.related_id,
            amount=transaction_data.amount,
            payment_method=transaction_data.payment_method,
            status="completed",  # Default to completed
            description=transaction_data.description
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def get_transaction(db: Session, transaction_id: int) -> Transaction:
        """Get transaction by ID."""
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    @staticmethod
    def get_user_transactions(db: Session, user_id: int, page: int = 1, limit: int = 10) -> tuple:
        """Get all transactions for a user."""
        skip = (page - 1) * limit
        total = db.query(Transaction).filter(Transaction.user_id == user_id).count()
        transactions = db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
        return transactions, total
    
    @staticmethod
    def get_all_transactions(db: Session, page: int = 1, limit: int = 10) -> tuple:
        """Get all transactions (admin only)."""
        skip = (page - 1) * limit
        total = db.query(Transaction).count()
        transactions = db.query(Transaction).order_by(
            Transaction.created_at.desc()
        ).offset(skip).limit(limit).all()
        return transactions, total
    
    @staticmethod
    def get_transactions_by_type(db: Session, transaction_type: str, page: int = 1, limit: int = 10) -> tuple:
        """Get transactions by type."""
        skip = (page - 1) * limit
        total = db.query(Transaction).filter(
            Transaction.transaction_type == transaction_type
        ).count()
        transactions = db.query(Transaction).filter(
            Transaction.transaction_type == transaction_type
        ).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
        return transactions, total
    
    @staticmethod
    def get_transactions_by_date_range(db: Session, start_date: datetime, end_date: datetime, 
                                      page: int = 1, limit: int = 10) -> tuple:
        """Get transactions within a date range."""
        skip = (page - 1) * limit
        total = db.query(Transaction).filter(
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date
        ).count()
        transactions = db.query(Transaction).filter(
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date
        ).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
        return transactions, total
    
    @staticmethod
    def get_report_summary(db: Session, start_date: datetime = None, end_date: datetime = None) -> dict:
        """Get transaction report summary."""
        query = db.query(Transaction)
        
        if start_date and end_date:
            query = query.filter(
                Transaction.created_at >= start_date,
                Transaction.created_at <= end_date
            )
        
        total_transactions = query.count()
        total_amount = sum([t.amount for t in query.all()]) if query.count() > 0 else 0
        
        # Count by type
        type_counts = {}
        for t_type in ["membership_purchase", "order_payment", "refund"]:
            count = query.filter(Transaction.transaction_type == t_type).count()
            type_counts[t_type] = count
        
        # Count by status
        status_counts = {}
        for status in ["completed", "pending", "failed", "refunded"]:
            count = query.filter(Transaction.status == status).count()
            status_counts[status] = count
        
        return {
            "total_transactions": total_transactions,
            "total_amount": total_amount,
            "by_type": type_counts,
            "by_status": status_counts
        }
