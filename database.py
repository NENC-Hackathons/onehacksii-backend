from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, ARRAY, create_engine
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
    name = Column(String(), unique=True)
    email = Column(String())
    password = Column(String())
    timestamp = Column(DateTime())
    
class UserIncomeIndex(Base):
    __tablename__ = 'userIncomeIndex'
    id = Column(Integer, primary_key=True)
    user = Column(ForeignKey('users.id'))
    income = Column(Float())
    incomeIndex = Column(Float())
    spendingType = Column(ForeignKey('spendingTypes.id'))
    
class SpendingType(Base):
    __tablename__ = 'spendingTypes'
    id = Column(Integer, primary_key=True)
    type = Column(Integer())
    name = Column(String())
    description = Column(String())
    recommendedSpendingRatio = Column(ARRAY(Float))

Base.metadata.create_all(bind=engine)