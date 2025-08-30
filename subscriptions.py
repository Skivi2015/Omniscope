"""Subscription management and billing logic for Omniscope."""

from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from database import User, Subscription
from auth import is_owner

class SubscriptionManager:
    """Manages user subscriptions and billing."""
    
    MONTHLY_FEE = 29.99
    
    @staticmethod
    def get_user_subscription(db: Session, user_id: int) -> Optional[Subscription]:
        """Get active subscription for a user."""
        return db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status == "active"
        ).first()
    
    @staticmethod
    def create_subscription(db: Session, user_id: int) -> Subscription:
        """Create a new subscription for a user."""
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=30)  # 30-day billing cycle
        next_payment = start_date + timedelta(days=30)
        
        subscription = Subscription(
            user_id=user_id,
            status="active",
            monthly_fee=SubscriptionManager.MONTHLY_FEE,
            start_date=start_date,
            end_date=end_date,
            last_payment_date=start_date,
            next_payment_date=next_payment
        )
        
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription
    
    @staticmethod
    def is_subscription_active(db: Session, user: User) -> bool:
        """Check if user has active subscription or is owner."""
        # Owner always has access
        if is_owner(user):
            return True
        
        subscription = SubscriptionManager.get_user_subscription(db, user.id)
        if not subscription:
            return False
        
        # Check if subscription is still valid
        now = datetime.utcnow()
        if subscription.end_date and now > subscription.end_date:
            # Subscription expired, update status
            subscription.status = "expired"
            db.commit()
            return False
        
        return subscription.status == "active"
    
    @staticmethod
    def renew_subscription(db: Session, user_id: int) -> bool:
        """Renew subscription (mock payment processing)."""
        subscription = SubscriptionManager.get_user_subscription(db, user_id)
        if not subscription:
            return False
        
        # Mock payment processing - in real implementation, integrate with Stripe/PayPal
        payment_successful = SubscriptionManager._process_payment(user_id, SubscriptionManager.MONTHLY_FEE)
        
        if payment_successful:
            now = datetime.utcnow()
            subscription.last_payment_date = now
            subscription.next_payment_date = now + timedelta(days=30)
            subscription.end_date = now + timedelta(days=30)
            subscription.status = "active"
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def cancel_subscription(db: Session, user_id: int) -> bool:
        """Cancel user subscription."""
        subscription = SubscriptionManager.get_user_subscription(db, user_id)
        if not subscription:
            return False
        
        subscription.status = "cancelled"
        db.commit()
        return True
    
    @staticmethod
    def _process_payment(user_id: int, amount: float) -> bool:
        """Mock payment processing. Replace with real payment gateway."""
        # For demo purposes, always return True
        # In production, integrate with Stripe, PayPal, etc.
        print(f"Processing payment for user {user_id}: ${amount}")
        return True
    
    @staticmethod
    def get_subscription_status(db: Session, user: User) -> dict:
        """Get detailed subscription status for a user."""
        if is_owner(user):
            return {
                "status": "owner",
                "access": True,
                "message": "Owner account - unlimited access"
            }
        
        subscription = SubscriptionManager.get_user_subscription(db, user.id)
        if not subscription:
            return {
                "status": "no_subscription",
                "access": False,
                "message": "No active subscription found"
            }
        
        now = datetime.utcnow()
        is_active = SubscriptionManager.is_subscription_active(db, user)
        
        if is_active:
            days_remaining = (subscription.end_date - now).days if subscription.end_date else 0
            return {
                "status": "active",
                "access": True,
                "end_date": subscription.end_date.isoformat() if subscription.end_date else None,
                "next_payment_date": subscription.next_payment_date.isoformat() if subscription.next_payment_date else None,
                "days_remaining": days_remaining,
                "monthly_fee": subscription.monthly_fee,
                "message": f"Active subscription - {days_remaining} days remaining"
            }
        else:
            return {
                "status": "expired",
                "access": False,
                "end_date": subscription.end_date.isoformat() if subscription.end_date else None,
                "message": "Subscription expired - please renew to continue using Omniscope"
            }