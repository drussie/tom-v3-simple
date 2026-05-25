from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    database_url: str = getenv("TOM_V3_DATABASE_URL", "sqlite+pysqlite:///./tom_v3_dev.db")
    create_db_on_startup: bool = getenv("TOM_V3_CREATE_DB_ON_STARTUP", "false").lower() == "true"


settings = Settings()
