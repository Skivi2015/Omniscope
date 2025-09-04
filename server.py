# FastAPI server for OmniScope
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import json
from agent import AGENTS

app = FastAPI()
security = HTTPBearer(auto_error=False)

# Optional Firebase Admin SDK setup for token validation
# Uncomment and configure if you want backend token validation
"""
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin (uncomment to enable)
# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        return None
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None
"""

@app.post('/solve')
async def solve(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    data = await request.json()
    bot = data.get('bot')
    task = data.get('task')
    user_info = data.get('user', {})
    
    if not bot or not task:
        raise HTTPException(status_code=400, detail="bot and task are required")
    
    if bot not in AGENTS:
        raise HTTPException(status_code=404, detail="bot not found")
    
    # Optional: Verify Firebase token (uncomment the function above to enable)
    # verified_user = await verify_firebase_token(credentials)
    # if not verified_user:
    #     raise HTTPException(status_code=401, detail="Invalid or missing authentication token")
    
    # Add user context to the agent response
    result = AGENTS[bot].act(task)
    
    # Include user info in response for debugging/logging
    if user_info:
        result['user_context'] = {
            'user_id': user_info.get('uid'),
            'user_email': user_info.get('email'),
            'user_name': user_info.get('displayName')
        }
    
    return result

@app.get('/health')
async def health():
    return {"status": "healthy", "available_bots": list(AGENTS.keys())}
