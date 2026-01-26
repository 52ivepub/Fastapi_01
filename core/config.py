
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import BaseModel


class DbSettings(BaseModel):
    url: str = "sqlite+aiosqlite:///./db.sqlite3"
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = "/home/yevgeniy/IT/Fastapi_01/certs/jwt-private.pem"
    public_key_path: Path = "/home/yevgeniy/IT/Fastapi_01/certs/jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    # db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    # db_echo: bool = False
    # db_echo: bool = True

settings = Setting()


