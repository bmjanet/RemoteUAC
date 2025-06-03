# backend/app/routes/install_requests.py

"""
The FastAPI route “takes in” these POST requests and deserializes them into a Pydantic model.
This code defines the API endpoints for managing install requests in a FastAPI application.
It includes endpoints to create a new install request, check the status of an existing request, and approve or deny a request.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db import crud, database
from app.models.request import InstallRequestCreate, InstallRequestRead, InstallRequestStatus

router = APIRouter(tags=["install_requests"])

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/request",
    response_model=InstallRequestRead,
    status_code=status.HTTP_201_CREATED,
)

def create_request(request_in: InstallRequestCreate, db: Session = Depends(get_db)):
    """
    Create a new install request.
    """
    request = crud.create_install_request(db, request_in)
    if not request:
        raise HTTPException(status_code=400, detail="Failed to create install request")
    return request

@router.get(
    "/status/{request_id}",
    response_model=InstallRequestRead,
)
def get_status(request_id: int, db: Session = Depends(get_db)):
    """
    Get the status of an install request by ID.
    """
    request = crud.get_install_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Install request not found")
    return request

@router.post(
    "/approve/{request_id}",
    response_model=InstallRequestRead,
)
def approve_request(request_id: int, approve: bool, db: Session = Depends(get_db)):
    request = crud.get_install_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Install request not found")
    updated_request = crud.update_install_request_status(db, request_id, InstallRequestStatus.APPROVED if approve else InstallRequestStatus.REJECTED)
    return updated_request
