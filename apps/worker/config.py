from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class WorkerSettings:
    database_url: str = getenv("TOM_V3_DATABASE_URL", "sqlite+pysqlite:///./tom_v3_dev.db")


settings = WorkerSettings()
