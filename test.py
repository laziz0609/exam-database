from library.db import engine
from library.models import Base


def create_tables():
    Base.metadata.create_all(bind=engine)


create_tables()
