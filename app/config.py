#TODO: move configuration functionality here
import os

class Config():
    def __init__(self) -> None:
        self.db_user = os.environ.get("POSTGRES_USER", 'admin')
        self.db_passwd = os.environ.get("POSTGRES_PASSWORD", 'top_secret')
        self.db_host = os.environ.get("POSTGRES_HOST", 'ps')
        self.db_name = os.environ.get("POSTGRES_DB", 'space_x')
        self.db_port = os.environ.get("POSTGRES_PORT", '5432')

    def from_dict(self) -> dict:
        return (
            self.db_user,
            self.db_passwd,
            self.db_host,
            self.db_name,
            self.db_port,
        )

    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_passwd}@{self.db_host}:{self.db_port}/{self.db_name}"
