from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from .loggers import logger

session = scoped_session(sessionmaker())
class BaseMixin(object):
    query = session.query_property()
Base = declarative_base(cls=BaseMixin)


def db_init(app):
    config = app["config"] or {}
    engine = create_engine(config["SQLALCHEMY_DATABASE_URI"])
    engine.echo = config["SQLALCHEMY_ECHO"]
    Base.metadata.bind = engine
    Base.metadata.create_all()
    session.configure(bind=engine)
    logger.info( "DATABASE CONFIGURED" )
