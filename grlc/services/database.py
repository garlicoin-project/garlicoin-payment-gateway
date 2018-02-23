from datetime import datetime
from sqlalchemy import engine_from_config, Column, String, ForeignKey, Numeric, Boolean, DateTime
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm
from uuid import uuid4

Base = dec.declarative_base()


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
