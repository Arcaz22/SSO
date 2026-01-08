from fastapi import APIRouter, Depends
from app.core.di import get_current_user
from app.domain.auth.entities import User
from app.presentation.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
