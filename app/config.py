#TODO: move configuration functionality here
import os

class Config():
    def __init__(self) -> None:
        self.db_user = os.environ["POSTGRES_USER"] or 'admin'
        self.db_passwd = os.environ["POSTGRES_PASSWORD"] or 'top_secret'
        self.db_host = os.environ["POSTGRES_HOST"] or 'ps'
        self.db_name = os.environ["POSTGRES_DB"] or 'space_x'
        self.db_port = os.environ["POSTGRES_PORT"] or '5432'

    def from_dict(self) -> dict:
        return (
            self.db_user,
            self.db_passwd,
            self.db_host,
            self.db_name,
            self.db_port,
        )

    def get_db_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_passwd}@\
            {self.db_host}:{self.db_port}/{self.db_name}"
