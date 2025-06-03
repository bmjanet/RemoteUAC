from fastapi import FastAPI
from app.routes.install_request import router as install_request_router

app = FastAPI(
    title="RemoteUAC backend",
    description="API for managing install requests and approvals for RemoteUAC.",
    version="0.1.0"
)

app.include_router(install_request_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "RemoteUAC backend is running!"}