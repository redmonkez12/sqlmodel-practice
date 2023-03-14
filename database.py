from sqlmodel import SQLModel, create_engine
from dotenv import dotenv_values


def connect():
    config = dotenv_values("../.env")
    username = config.get("DB_USERNAME")
    password = config.get("DB_PASSWORD")
    dbname = config.get("DB_NAME")

    db_url = f"postgresql+psycopg2://{username}:{password}@localhost:5432/{dbname}"

    engine = create_engine(db_url, echo=True, future=True)

    return engine


def create_tables(engine):
    SQLModel.metadata.drop_all(engine, checkfirst=True)
    SQLModel.metadata.create_all(engine, checkfirst=True)
