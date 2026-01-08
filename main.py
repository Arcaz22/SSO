from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.http.routes.users import router as users_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="SSO",
    description="API SSO",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)

@app.get("/")
async def root():
    return {
        "message": "SSO",
        "docs": "/docs",
        "status": "online"
    }
