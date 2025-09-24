from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.keys import KeyListResponse, KeySearchRequest, KeyDetailResponse
from app.models.key_schemas import CreateKeyRequest, CreateKeyResponse, DeleteKeyRequest, DeleteKeyResponse
from app.services.cloudhsm_service import CloudHSMService
from app.utils.auth_dependency import get_current_user

router = APIRouter(prefix="/keys", tags=["keys"])

@router.get("/", response_model=KeyListResponse)
@router.get("", response_model=KeyListResponse)
async def list_keys(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """List all keys in CloudHSM"""
    
    # Initialize CloudHSM service
    hsm_service = CloudHSMService()
    
    # Get keys using stored credentials
    keys = hsm_service.list_keys(current_user.username, current_user.password)
    
    return KeyListResponse(
        keys=keys,
        count=len(keys)
    )

@router.post("/", response_model=KeyListResponse)
async def filter_keys(search_request: KeySearchRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Filter keys and return KeyInfo list for client-side filtering"""
    
    # Initialize CloudHSM service
    hsm_service = CloudHSMService()
    
    # Filter keys using search criteria
    keys = hsm_service.filter_keys(
        current_user.username, 
        current_user.password,
        search_request.key_class,
        search_request.key_type,
        search_request.label,
        search_request.key_id
    )
    
    return KeyListResponse(
        keys=keys,
        count=len(keys)
    )

@router.post("/find", response_model=KeyDetailResponse)
async def find_key(search_request: KeySearchRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Find specific key with detailed attributes"""
    
    # Initialize CloudHSM service
    hsm_service = CloudHSMService()
    
    # Find key using filters
    key_detail = hsm_service.find_key(
        current_user.username, 
        current_user.password,
        search_request.key_class,
        search_request.key_type,
        search_request.label,
        search_request.key_id
    )
    
    if not key_detail:
        raise HTTPException(status_code=404, detail="Key not found")
    
    return key_detail

@router.post("/create", response_model=CreateKeyResponse)
async def create_key(create_request: CreateKeyRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new key in CloudHSM"""
    
    # Initialize CloudHSM service
    hsm_service = CloudHSMService()
    
    # Create key
    result = hsm_service.create_key(
        current_user.username,
        current_user.password,
        create_request
    )
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return result

@router.post("/delete", response_model=DeleteKeyResponse)
async def delete_key(delete_request: DeleteKeyRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete key(s) from CloudHSM"""
    
    # Initialize CloudHSM service
    hsm_service = CloudHSMService()
    
    # Delete key
    result = hsm_service.delete_key(
        current_user.username,
        current_user.password,
        delete_request
    )
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    return result