# backend/app/models/request.py

from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class InstallRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"

class InstallRequestBase(BaseModel):
    device_id: str
    app_name: str
    size: str
    path: str
    download_source: str
    requested_changes: Dict[str, Any]  # e.g., {"PATH": True, "Registry": ["HKLM\\…"]}
    timestamp: datetime

class InstallRequestCreate(InstallRequestBase):
    pass

class InstallRequestRead(InstallRequestBase):
    id: int
    status: InstallRequestStatus

    class Config:
        orm_mode = True
