import logging
from typing import AsyncGenerator
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.infrastructure.db import AsyncSessionLocal
from app.infrastructure.db.repositories import SqlAlchemyUserRepository
from app.infrastructure.keycloak.client import KeycloakProvider
from app.domain.auth.entities import User

from app.application.usecases.auth import GetCurrentUserUseCase

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

def get_user_repo(session: AsyncSession) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)

@lru_cache(maxsize=1)
def get_auth_provider() -> KeycloakProvider:
    return KeycloakProvider()

def build_get_current_user_uc(session: AsyncSession) -> GetCurrentUserUseCase:
    return GetCurrentUserUseCase(
        user_repo=get_user_repo(session),
        auth_provider=get_auth_provider()
    )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing",
        )

    token = credentials.credentials

    uc = build_get_current_user_uc(session)

    try:
        user = await uc.execute(token)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
