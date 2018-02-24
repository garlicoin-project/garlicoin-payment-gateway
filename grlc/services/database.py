from datetime import datetime
from grlc.services.log_service import LogService
from sqlalchemy import engine_from_config, Column, String, ForeignKey, Numeric, Boolean, DateTime
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm
from uuid import uuid4

Base = dec.declarative_base()
logger = LogService.logger


class User(Base):
    __tablename__ = 'User'

    id = Column(String, primary_key=True, default=uuid4)
    email = Column(String)
    grlc_address = Column(String)
    created = Column(DateTime, default=datetime.now)
    validated = Column(Boolean)

    transactions = sqlalchemy.orm.relationship('Transaction', back_populates='user')


class Transaction(Base):
    __tablename__ = 'Transaction'

    id = Column(String, primary_key=True, default=uuid4)
    payment_address = Column(String, ForeignKey('Address.address'))
    payment_amount = Column(Numeric)
    payment_amount_string = Column(String)
    user_id = Column(String, ForeignKey(column='User.id'), nullable=False)
    opened = Column(DateTime, default=datetime.now)
    received = Column(DateTime)
    status = Column(String)

    user = sqlalchemy.orm.relationship('User', back_populates='transactions')
    address = sqlalchemy.orm.relationship('Address', back_populates='transactions')


class Address(Base):
    __tablename__ = 'Address'

    address = Column(String, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    last_used = Column(DateTime)
    balance_date = Column(DateTime)
    balance = Column(Numeric)

    transactions = sqlalchemy.orm.relationship('Transaction', back_populates='address')


class DbSession:
    factory = None

    @staticmethod
    def create_session() -> sqlalchemy.orm.Session:
        if DbSession.factory is None:
            raise ConnectionError('create_session called without factory initialized')
        return DbSession.factory()

    def __init__(self):
        self.session = self.factory()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.warning(f'DB Error {exc_type}: {exc_val}')
            self.session.rollback()
        self.session.close()


def includeme(config):
    settings = config.get_settings()
    engine = engine_from_config(configuration=settings, prefix='sqlalchemy.', echo=False)

    Base.metadata.create_all(engine)
    session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
    DbSession.factory = sqlalchemy.orm.scoped_session(session_factory=session_factory)
