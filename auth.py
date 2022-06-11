from datetime import timedelta,datetime
from multiprocessing.pool import ApplyResult
from jose import jwt
from passlib.context import CryptContext
from config import secret
from database import session as db

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def CredentialsAreFree(email:str,name:str):
    if db.execute(f"SELECT * FROM users WHERE email = :email OR name = :name",{'email':email,'name':name}).length > 0:
        return False
    return True

def CredentialsAreTrue(name:str,password:str):
    if db.execute(f"SELECT * FROM users WHERE name = :name AND password = :password",{'name':name,'password':context.hash(password)}).length > 0:
        return True
    return False

def CreateToken(name:str):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=14),
        'iat': datetime.utcnow(),
        'name': name
    }
    return jwt.encode(payload, secret, algorithm='HS256')

def DecodeToken(token:str):
    return jwt.decode(token, secret, algorithms=['HS256'])

def CalculateUserAxis(name:str,income:float,questions:list):
    startValue = 0.5
    multiplier = 1
    if income < 500000.0 and income >= 80000.0:
        multiplier = 0.75
    elif income < 80000.0 and income >= 25000.0:
        multiplier = 0.5
    elif income < 25000.0:
        multiplier = 0.25
    appendValue = sum(questions)/5/2*multiplier
    
    return