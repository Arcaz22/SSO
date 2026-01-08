from app.domain.auth.ports import IUserRepository, IAuthProvider
from app.domain.auth.entities import User
from app.domain.auth.rules import InvalidTokenError

class GetCurrentUserUseCase:
    def __init__(self, user_repo: IUserRepository, auth_provider: IAuthProvider):
        self.user_repo = user_repo
        self.auth_provider = auth_provider

    async def execute(self, token: str) -> User:
        try:
            user_info = self.auth_provider.verify_token(token)
        except Exception as e:
            raise InvalidTokenError(f"Token validation failed: {str(e)}")

        keycloak_id = user_info.get("sub")
        email = user_info.get("email")
        username = user_info.get("preferred_username")

        local_user = await self.user_repo.get_by_id(keycloak_id)

        if not local_user:
            new_user = User(
                id=keycloak_id,
                email=email,
                username=username,
                full_name=user_info.get("name"),
            )
            local_user = await self.user_repo.create(new_user)

        return local_user
