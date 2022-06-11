from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database
from config import url

def engine():
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url,pool_size=50,echo=False)
    return engine

engine = engine()

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    email = Column(String())
    password = Column(String())
    devices = Column(Integer())
    
class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    user = Column(ForeignKey('users.id'))
    name = Column(String())
    description = Column(String())
    powerConsupmption = Column(String())
    timestamp = Column(String())

Base.metadata.create_all(bind=engine)