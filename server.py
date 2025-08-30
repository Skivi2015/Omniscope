# FastAPI server for OmniScope with subscription system
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta
from agent import AGENTS
from database import get_db, create_tables, init_owner, User, Subscription
from auth import authenticate_user, create_access_token, get_current_user, hash_password
from subscriptions import SubscriptionManager

# Initialize database and owner account
create_tables()
init_owner()

app = FastAPI(title="OmniScope API", description="AI Bot Service with Subscription System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="web"), name="static")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class SolveRequest(BaseModel):
    bot: str
    task: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Authentication endpoints
@app.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and create their subscription."""
    # Check if username already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create subscription for new user
    SubscriptionManager.create_subscription(db, new_user.id)
    
    # Create access token
    access_token_expires = timedelta(minutes=1440)  # 24 hours
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    authenticated_user = authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=1440)  # 24 hours
    access_token = create_access_token(
        data={"sub": authenticated_user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Subscription endpoints
@app.get("/subscription/status")
async def subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's subscription status."""
    return SubscriptionManager.get_subscription_status(db, current_user)

@app.post("/subscription/renew")
async def renew_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Renew user's subscription."""
    if current_user.is_owner:
        raise HTTPException(
            status_code=400,
            detail="Owner account doesn't need subscription renewal"
        )
    
    success = SubscriptionManager.renew_subscription(db, current_user.id)
    if success:
        return {"message": "Subscription renewed successfully"}
    else:
        raise HTTPException(
            status_code=400,
            detail="Failed to renew subscription"
        )

@app.post("/subscription/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel user's subscription."""
    if current_user.is_owner:
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel owner account"
        )
    
    success = SubscriptionManager.cancel_subscription(db, current_user.id)
    if success:
        return {"message": "Subscription cancelled successfully"}
    else:
        raise HTTPException(
            status_code=400,
            detail="Failed to cancel subscription"
        )

# Protected bot endpoint
@app.post('/solve')
async def solve(
    request: SolveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Solve a task using specified bot (requires active subscription)."""
    # Check subscription status
    if not SubscriptionManager.is_subscription_active(db, current_user):
        raise HTTPException(
            status_code=403,
            detail="Active subscription required to use bots"
        )
    
    # Check if bot exists (Note: AGENTS dict has 'bots' key based on our earlier exploration)
    if 'bots' not in AGENTS:
        return {'error': 'bots not found'}
    
    # For now, all bots use the same agent since the structure needs to be fixed
    return AGENTS['bots'].act(f"{request.bot}: {request.task}")

# Legacy endpoint for backward compatibility (will require authentication)
@app.post('/solve_legacy')
async def solve_legacy(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Legacy solve endpoint (requires active subscription)."""
    # Check subscription status
    if not SubscriptionManager.is_subscription_active(db, current_user):
        raise HTTPException(
            status_code=403,
            detail="Active subscription required to use bots"
        )
    
    data = await request.json()
    bot = data.get('bot')
    task = data.get('task')
    
    if 'bots' in AGENTS:
        return AGENTS['bots'].act(f"{bot}: {task}")
    return {'error': 'bots not found'}

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface."""
    with open("web/index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "omniscope"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
