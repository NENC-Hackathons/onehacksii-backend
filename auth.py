from datetime import timedelta,datetime
from jwt import encode, decode
from passlib.context import CryptContext
from config import secret
from database import session as db

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def CredentialsAreFree(email:str,name:str):
    areFree = db.execute(f"SELECT * FROM users WHERE email = :email OR name = :name",{'email':email,'name':name}).fetchall()
    if len(areFree) > 0:
        return False
    return True

def HashPassword(password:str):
    return context.hash(password)

def CredentialsAreTrue(name:str,password:str):

    areTrue = db.execute(f"SELECT * FROM users WHERE name = :name AND password = :password",{'name':name,'password':context.hash(password)}).fetchall()
    if len(areTrue) > 0:
        return True
    return False

def CreateToken(name:str):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=14),
        'iat': datetime.utcnow(),
        'name': name
    }
    return encode(payload, secret, algorithm='HS256')

def DecodeToken(token:str):
    return decode(token, secret, algorithms=['HS256'])

def CalculateUserAxis(name:str,income:int,questions:list):
    multiplier = calculateIncomeIndex(income)
    spendingIndex = sum(questions)/5/2*multiplier #based on the 5 question answers it returns the average number of the array then multiplies it by the income index to get the spending index that is based on the income
    spendingPercentages(spendingIndex) # wants(clothes,cars,electronics,vanity items, etc..)/needs(bills,food,utilities,etc..)/investments(stocks,real estate,etc..)
    return

def calculateIncomeIndex(income:int):
    return income/500000

def spendingPercentages(spendingIndex:float):
    savings = spendingIndex * 0.95
    #1  = needs + wants + savings
    return

datatable = ([0.05,0.35,0.6], [0.1,0.35,0.55], [0.2,0.35,0.45], [0.3,0.3,0.4], [0.4,0.3,0.3], [0.5,0.3,0.2], [0.6,0.3,0.1], [0.7,0.2,0.1], [0.75,0.15,0.1], [0.8,0.15,0.05], [0.9,0.1,0.05])