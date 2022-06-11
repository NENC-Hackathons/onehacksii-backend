from datetime import timedelta,datetime
from jose import jwt
from passlib.context import CryptContext
from config import secret
from database import session as db

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def CredentialsAreFree(email,name):
    if db.execute(f"SELECT * FROM users WHERE email = :email OR name = :name",{'email':email,'name':name}).length > 0:
        return False
    return True

def CredentialsAreTrue(name,password):
    if db.execute(f"SELECT * FROM users WHERE name = :name AND password = :password",{'name':name,'password':context.hash(password)}).length > 0:
        return True
    return False

def CreateToken(name):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=14),
        'iat': datetime.utcnow(),
        'name': name
    }
    return jwt.encode(payload, secret, algorithm='HS256')