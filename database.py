"""Database models and configuration for Omniscope subscription system."""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./subscriptions.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_owner = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    status = Column(String, default="active")  # active, expired, cancelled
    monthly_fee = Column(Float, default=29.99)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    last_payment_date = Column(DateTime, nullable=True)
    next_payment_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_owner():
    """Initialize the owner account if it doesn't exist."""
    from auth import hash_password
    
    db = SessionLocal()
    try:
        # Check if owner exists
        owner = db.query(User).filter(User.is_owner == True).first()
        if not owner:
            # Create owner account with default credentials
            owner_username = os.getenv("OWNER_USERNAME", "admin")
            owner_email = os.getenv("OWNER_EMAIL", "admin@omniscope.com")
            owner_password = os.getenv("OWNER_PASSWORD", "omniscope_admin_2024")
            
            owner = User(
                username=owner_username,
                email=owner_email,
                hashed_password=hash_password(owner_password),
                is_owner=True
            )
            db.add(owner)
            db.commit()
            print(f"Owner account created: {owner_username}")
        else:
            print(f"Owner account exists: {owner.username}")
    finally:
        db.close()