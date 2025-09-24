from sqlalchemy.orm import Session
from app.models.database import UserSession
from datetime import datetime

class SessionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_or_update_session(self, username: str, password: str) -> UserSession:
        """Create new session or update existing one"""
        # Delete any existing sessions for this user
        self.db.query(UserSession).filter(UserSession.username == username).delete()
        
        # Create new session
        session = UserSession.create_session(username, password)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_session(self, username: str, session_id: str) -> UserSession:
        """Get session by username and session_id"""
        return self.db.query(UserSession).filter(
            UserSession.username == username,
            UserSession.session_id == session_id
        ).first()
    
    def validate_session(self, username: str, session_id: str) -> UserSession:
        """Validate session and return if valid, None if expired/invalid"""
        session = self.get_session(username, session_id)
        if not session:
            return None
        
        if session.is_expired():
            # Clean up expired session
            self.db.delete(session)
            self.db.commit()
            return None
        
        return session
    
    def delete_session(self, username: str, session_id: str):
        """Delete specific session"""
        session = self.get_session(username, session_id)
        if session:
            self.db.delete(session)
            self.db.commit()
    
    def cleanup_expired_sessions(self):
        """Clean up all expired sessions"""
        expired_sessions = self.db.query(UserSession).filter(
            UserSession.expiry < datetime.utcnow()
        )
        expired_sessions.delete()
        self.db.commit()