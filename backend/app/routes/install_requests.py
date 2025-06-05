# backend/app/routes/install_requests.py

"""
The FastAPI route “takes in” these POST requests and deserializes them into a Pydantic model.
This code defines the API endpoints for managing install requests in a FastAPI application.
It includes endpoints to create a new install request, check the status of an existing request, and approve or deny a request.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Header
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

# Dependency to get the current admin user from the authorization header
# This function checks the token and ensures the user has admin privileges.
# If the token is invalid or the user is not an admin, it raises an HTTPException with a 401 status code.
#
# # Params:
# - authorization: The authorization header containing the JWT token.
# Returns:
# - The payload of the token if valid and the user is an admin.
def get_current_admin(authorization: str = Header(..., alias="Authorization")):
    token = authorization.split(" ")[-1] if " " in authorization else authorization
    payload = crud.verify_token(token)
    if payload is None or payload.get("sub") != "admin_user":
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token, or insufficient permissions",
        )
    return payload 

@router.post(
    "/request",
    response_model=InstallRequestRead,
    status_code=status.HTTP_201_CREATED,
)
def create_request(request_in: InstallRequestCreate, db: Session = Depends(get_db)):
    """
    Create a new install request.

    - **device_id**: Unique identifier for the device.
    - **app_name**: Name of the application to install.
    - **size**: Size of the installer.
    - **path**: Path where the installer is located.
    - **download_source**: URL to download the installer.
    - **requested_changes**: Dictionary of requested system changes.
    - **timestamp**: Time of the request.
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

    - **request_id**: The ID of the install request.
    """
    request = crud.get_install_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Install request not found")
    return request



# Approve or reject an install request
# This endpoint allows an admin to approve or reject an install request.
@router.post(
    "/approve/{request_id}",
    response_model=InstallRequestRead,
)
def approve_request(request_id: int, approve: bool, db: Session = Depends(get_db), _: dict = Depends(get_current_admin)):
    """
    Approve or reject an install request.

    - **request_id**: The ID of the install request.
    - **approve**: Set to `true` to approve, `false` to reject.
    - **Authorization**: Bearer token for admin authentication.
    """
    request = crud.get_install_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Install request not found")
    updated_request = crud.update_request_status(db, request_id, InstallRequestStatus.APPROVED if approve else InstallRequestStatus.REJECTED)
    return updated_request
