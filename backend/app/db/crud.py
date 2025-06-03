# backend/app/db/crud.py

from sqlalchemy.orm import Session
from app.models.request import InstallRequestCreate, InstallRequestStatus
from app.db.database import Base, engine
from sqlalchemy import Column, Integer, String, Enum, JSON, DateTime
from sqlalchemy.sql import func
import app.db.database as database_module

# Declare the ORM model for install_requests table
class InstallRequestORM(Base):
    __tablename__ = "install_requests"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    app_name = Column(String)
    size = Column(String)
    path = Column(String)
    download_source = Column(String)
    requested_changes = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(InstallRequestStatus), default=InstallRequestStatus.PENDING)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


def create_install_request(db: Session, req: InstallRequestCreate):
    db_req = InstallRequestORM(
        device_id=req.device_id,
        app_name=req.app_name,
        size=req.size,
        path=req.path,
        download_source=req.download_source,
        requested_changes=req.requested_changes,
        timestamp=req.timestamp,
    )
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

def get_install_request(db: Session, request_id: int):
    return db.query(InstallRequestORM).filter(InstallRequestORM.id == request_id).first()

def update_request_status(db: Session, request_id: int, new_status: InstallRequestStatus):
    req_obj = db.query(InstallRequestORM).filter(InstallRequestORM.id == request_id).first()
    if not req_obj:
        return None
    req_obj.status = new_status
    db.commit()
    db.refresh(req_obj)
    return req_obj

