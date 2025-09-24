import base64
from fastapi import Cookie, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db, UserSession
from app.services.session_service import SessionService

def get_current_user(session: str = Cookie(None), db: Session = Depends(get_db)) -> UserSession:
    """Dependency to get current authenticated user from session cookie"""
    if not session:
        raise HTTPException(status_code=401, detail="No session cookie found")
    
    try:
        # Decode base64 session cookie
        session_decoded = base64.b64decode(session.encode()).decode()
        
        # Parse username:session_id
        if ":" not in session_decoded:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        username, session_id = session_decoded.split(":", 1)
        
        if not username or not session_id:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        # Validate session in database
        session_service = SessionService(db)
        user_session = session_service.validate_session(username, session_id)
        
        if not user_session:
            raise HTTPException(status_code=401, detail="Session expired or invalid")
        
        return user_session
        
    except base64.binascii.Error:
        raise HTTPException(status_code=401, detail="Invalid session encoding")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")