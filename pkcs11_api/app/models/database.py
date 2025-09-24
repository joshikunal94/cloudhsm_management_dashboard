from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import uuid

Base = declarative_base()

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    username = Column(String, primary_key=True)
    session_id = Column(String, primary_key=True)
    password = Column(String, nullable=False)  # Plaintext for CloudHSM operations
    expiry = Column(DateTime, nullable=False)
    
    @classmethod
    def create_session(cls, username: str, password: str, hours: int = 8):
        """Create new session with expiry"""
        return cls(
            username=username,
            session_id=str(uuid.uuid4()),
            password=password,
            expiry=datetime.utcnow() + timedelta(hours=hours)
        )
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expiry

# Database setup
DATABASE_URL = "sqlite:///./cloudhsm_sessions.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()