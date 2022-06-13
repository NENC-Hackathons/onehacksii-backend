from datetime import timedelta,datetime
from operator import and_
from jwt import encode, decode
from passlib.context import CryptContext
from config import secret
from database import SpendingType, User, session as db

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def CredentialsAreFree(email:str,name:str):
    areFree = db.execute(f"SELECT * FROM users WHERE email = :email OR name = :name",{'email':email,'name':name})
    for user in areFree:
        if user:
            return False

def HashPassword(password:str):
    return context.hash(password)

def CredentialsAreTrue(name:str,password:str):
    areTrue = db.execute(f"SELECT * FROM users WHERE name = :name",{'name':name}).first()
    if context.verify(password,areTrue.password):
        return True
    return False

def CreateToken(name:str):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=14),
        'iat': datetime.utcnow(),
        'name': name
    }
    return encode(payload, secret, algorithm='HS256')

def GetUserByToken(token:str):
    data = decode(token, secret, algorithms=['HS256'])
    if data['exp'] > datetime.utcnow():
        user = db.execute(f"SELECT * FROM users WHERE name = :name",{'name':data['name']}).first()
        if user:
            return user
        return False

def getBudgetSet(income:int,questionSum:int):
    multiplier = calculateIncomeIndex(income)
    spendingIndex = round(questionSum/6/2*multiplier,1)*10
    return int(spendingIndex)
    
def calculateIncomeIndex(income:int):
    return income/500000

budgetSets = [[0.05,0.35,0.6], [0.1,0.35,0.55], [0.2,0.35,0.45], [0.3,0.3,0.4], [0.4,0.3,0.3], [0.5,0.3,0.2], [0.6,0.3,0.1], [0.7,0.2,0.1], [0.75,0.15,0.1], [0.8,0.15,0.05], [0.9,0.1,0.05]]