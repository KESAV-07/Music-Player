from sqlmodel import create_engine, SQLModel

DATABASE_NAME = "song.db"
engine = create_engine(f"sqlite:///{DATABASE_NAME}")


def create_tables():
    SQLModel.metadata.create_all(engine)