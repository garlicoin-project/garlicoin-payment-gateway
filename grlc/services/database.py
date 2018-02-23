from sqlalchemy import engine_from_config, Column, String
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm

Base = dec.declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(String, primary_key=True)


class DbSessionFactory:
    factory = None

    @staticmethod
    def create_session() -> sqlalchemy.orm.Session:
        if DbSessionFactory.factory is None:
            raise ConnectionError('create_session called without factory initialized')

        return DbSessionFactory.factory()


def init_script(settings: dict):
    engine = engine_from_config(configuration=settings, prefix='sqlalchemy.', echo=False)

    Base.metadata.create_all(engine)
    session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
    DbSessionFactory.factory = sqlalchemy.orm.scoped_session(session_factory=session_factory)


def includeme(config):
    settings = config.get_settings()
    init_script(settings=settings)
