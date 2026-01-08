from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError

from app.core.settings import settings
from app.domain.auth.ports import IAuthProvider
from app.domain.auth.rules import InvalidTokenError, AuthError

class KeycloakProvider(IAuthProvider):
    def __init__(self):
        self.client = KeycloakOpenID(
            server_url=settings.keycloak_url,
            client_id=settings.keycloak_client_id,
            realm_name=settings.keycloak_realm,
            client_secret_key=settings.keycloak_client_secret,
        )

    def verify_token(self, token: str) -> dict:
        if not token or token == "undefined":
            raise InvalidTokenError("Token missing")

        try:
            token_info = self.client.introspect(token)

            if not token_info.get("active"):
                raise InvalidTokenError("Token is not active or has been revoked")

            return token_info

        except KeycloakAuthenticationError as e:
            raise InvalidTokenError(f"Authentication failed: {str(e)}")

        except KeycloakGetError as e:
            raise AuthError(f"Keycloak connection error: {str(e)}")

        except Exception as e:
            raise InvalidTokenError(f"Token validation failed: {str(e)}")
