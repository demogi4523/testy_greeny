from sqlalchemy import create_engine, MetaData
from databases import Database


# FIXME: create single interface for script, cli and main modules
def get_db(db_url: str, metadata: MetaData = MetaData()):
    database = Database(db_url)
    engine = create_engine(db_url)
    metadata.create_all(engine)

    return database, metadata
