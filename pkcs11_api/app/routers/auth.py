import base64
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from app.models.auth import LoginRequest, LoginResponse
from app.models.database import get_db
from app.services.cloudhsm_service import CloudHSMService
from app.services.session_service import SessionService
from app.utils.auth_dependency import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """Authenticate user with CloudHSM and create database session"""
    
    # Initialize CloudHSM service
    hsm_service = CloudHSMService()
    
    # Authenticate with CloudHSM
    if not hsm_service.authenticate_user(login_request.username, login_request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create/update session in database
    session_service = SessionService(db)
    user_session = session_service.create_or_update_session(
        login_request.username, 
        login_request.password
    )
    
    # Create base64 encoded session cookie (username:session_id)
    session_string = f"{user_session.username}:{user_session.session_id}"
    session_encoded = base64.b64encode(session_string.encode()).decode()
    
    # Set cookie with UTC datetime
    expires_utc = user_session.expiry.replace(tzinfo=timezone.utc)
    response.set_cookie(
        key="session",
        value=session_encoded,
        expires=expires_utc,
        httponly=True,
        samesite="lax"
    )
    
    # Cleanup HSM session
    hsm_service.logout()
    
    return LoginResponse(
        success=True,
        message="Login successful",
        session_expires=user_session.expiry.isoformat()
    )

@router.post("/logout", response_model=LoginResponse)
async def logout(response: Response, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user and clear session"""
    
    # Delete session from database
    session_service = SessionService(db)
    session_service.delete_session(current_user.username, current_user.session_id)
    
    # Clear cookie
    response.delete_cookie(key="session")
    
    return LoginResponse(
        success=True,
        message="Logout successful"
    )

@router.get("/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return {
        "username": current_user.username,
        "session_id": current_user.session_id,
        "expires": current_user.expiry.isoformat()
    }