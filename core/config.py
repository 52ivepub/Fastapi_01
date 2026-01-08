from pydantic_settings import BaseSettings
from pydantic import BaseModel


class DbSettings(BaseModel):
    url: str = "sqlite+aiosqlite:///./db.sqlite3"
    echo: bool = True

class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()
    # db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    # db_echo: bool = False
    # db_echo: bool = True

settings = Setting()


