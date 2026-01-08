from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.domain.auth.ports import IUserRepository
from app.domain.auth.entities import User
from app.infrastructure.db.models import MstUser

class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> Optional[User]:
        query = select(MstUser).where(MstUser.id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalars().first()

        if user_model:
            return user_model.to_domain()
        return None

    async def create(self, user: User) -> User:
        user_model = MstUser.from_domain(user)

        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)

        return user_model.to_domain()

    async def update(self, user: User) -> User:
        pass
