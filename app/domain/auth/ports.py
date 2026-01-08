from abc import ABC, abstractmethod
from typing import Optional
from app.domain.auth.entities import User

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

class IAuthProvider(ABC):
    @abstractmethod
    def verify_token(self, token: str) -> dict:
        pass
