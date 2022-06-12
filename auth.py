from datetime import timedelta,datetime
from jwt import encode, decode
from passlib.context import CryptContext
from config import secret
from database import session as db

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def CredentialsAreFree(email:str,name:str):
    areFree = db.execute(f"SELECT * FROM users WHERE email = :email OR name = :name",{'email':email,'name':name})
    for user in areFree:
        return False
    return True

def HashPassword(password:str):
    return context.hash(password)

def CredentialsAreTrue(name:str,password:str):
    areTrue = db.execute(f"SELECT * FROM users WHERE name = :name",{'name':name})
    for user in areTrue:
        if context.verify(password,user.password):
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

def CalculateUserAxis(name:str,income:int,questionSum:int):
    multiplier = calculateIncomeIndex(income)
    spendingIndex = round(questionSum/6/2*multiplier,1)*10
    
    return

def calculateIncomeIndex(income:int):
    return income/500000
