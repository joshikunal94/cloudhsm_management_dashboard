from pydantic import BaseModel
from typing import List, Optional

class KeyInfo(BaseModel):
    key_class: str  # PUBLIC_KEY, PRIVATE_KEY, SECRET_KEY
    key_type: str   # RSA, AES, EC
    label: Optional[str] = None
    key_id: Optional[str] = None

class KeyListResponse(BaseModel):
    keys: List[KeyInfo]
    count: int

class KeySearchRequest(BaseModel):
    key_class: Optional[str] = None
    key_type: Optional[str] = None
    label: Optional[str] = None
    key_id: Optional[str] = None

class KeyDetailResponse(BaseModel):
    key_class: str
    key_type: str
    label: Optional[str] = None
    key_id: Optional[str] = None
    token: bool
    private: bool
    sensitive: bool
    extractable: bool
    local: bool
    modifiable: bool
    destroyable: bool