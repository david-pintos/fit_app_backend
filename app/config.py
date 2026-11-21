from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    class Settings: load settings from environment file.
        @secret_key: a key must be generated with the command 'openssl rand -hex 32' for JWT tokens.
        @hash_algorithm: algorithm for signing JWT tokens.
        @access_token_expire_days: Expire days of generated tokens
    """

    model_config = SettingsConfigDict(
        env_file="settings.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )

    # Authentication
    secret_key: str
    hash_algorithm: str = "HS256"
    access_token_expire_days: int = 30


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
