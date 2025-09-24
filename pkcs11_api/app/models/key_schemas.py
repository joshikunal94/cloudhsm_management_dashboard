from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum

class KeyClass(str, Enum):
    SECRET_KEY = "SECRET_KEY"
    PRIVATE_KEY = "PRIVATE_KEY"
    PUBLIC_KEY = "PUBLIC_KEY"

class KeyType(str, Enum):
    AES = "AES"
    RSA = "RSA"
    EC = "EC"

class CreateKeyRequest(BaseModel):
    label: str = Field(..., description="Key label")
    key_class: KeyClass = Field(..., description="Key class")
    key_type: KeyType = Field(..., description="Key type")
    key_size: Optional[int] = Field(None, description="Key size in bits (RSA) or bytes (AES)")
    token: bool = Field(True, description="Store key on token")
    private: bool = Field(True, description="Key is private")
    sensitive: bool = Field(True, description="Key is sensitive")
    extractable: bool = Field(False, description="Key is extractable")
    encrypt: Optional[bool] = Field(None, description="Key can encrypt")
    decrypt: Optional[bool] = Field(None, description="Key can decrypt")
    sign: Optional[bool] = Field(None, description="Key can sign")
    verify: Optional[bool] = Field(None, description="Key can verify")

class DeleteKeyRequest(BaseModel):
    label: Optional[str] = Field(None, description="Key label")
    key_id: Optional[str] = Field(None, description="Key ID")
    key_class: Optional[KeyClass] = Field(None, description="Key class")
    key_type: Optional[KeyType] = Field(None, description="Key type")

class CreateKeyResponse(BaseModel):
    success: bool
    message: str

class DeleteKeyResponse(BaseModel):
    success: bool
    message: str
    deleted_count: int = 0