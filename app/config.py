from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    oauth2_secret_key: str
    oauth2_algorithm: str
    oauth2_access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
