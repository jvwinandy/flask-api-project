from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

import logging

from settings import DATABASE_PATH

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(DATABASE_PATH)
session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = session.query_property()


def init_db():
    # import all modules here that might define models so that they will be registered properly on the metadata.
    Base.metadata.create_all(bind=engine)
