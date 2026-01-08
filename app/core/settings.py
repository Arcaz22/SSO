from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")

    keycloak_url: str = Field(..., alias="KEYCLOAK_URL")
    keycloak_realm: str = Field(..., alias="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(..., alias="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str = Field(..., alias="KEYCLOAK_CLIENT_SECRET")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

settings = Settings()
