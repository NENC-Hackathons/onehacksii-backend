from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import CreateToken, CredentialsAreFree, CredentialsAreTrue, GetUserByToken, HashPassword, getBudgetSet, budgetSets
from database import SpendingType, User, UserIncomeIndex, session as db
from schemes import BudgetSchema, Token, CredentialSchema

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"]
)

@app.get("/")
def main():
    return {"message": "Hello World"}
@app.post("/users/register")
async def register(data: CredentialSchema):
    if CredentialsAreFree(data.email,data.username):
        user = User(name=data.username,email=data.email,password=HashPassword(data.password))
        try:
            db.add(user)
            db.commit()
        except:
            db.rollback()
        token = CreateToken(data.username)
        return {'code':200,'message':'User created successfully','token':token,'username':data.username}
    return {'code':400,'message':'User already exists','token':None,'username':None}

@app.post("/users/login")
async def login(data: CredentialSchema):
    if CredentialsAreTrue(data.username,data.password):
        token = CreateToken(data.username)
        return {'code':200,'message':'User logged in successfully','token':token,'username':data.username}
    return {'code':401,'message':'Wrong Credentials','token':None,'username':None}

@app.post('/users/{name}/get')
async def getUser(data:Token):
    user = GetUserByToken(data.token)
    return { 'code':200,'message':'User found','user':user}

@app.post('/users/{name}/budgetCalculate')
async def budgetCalculate(data:BudgetSchema):
    user = db.execute(f"SELECT * FROM users WHERE name = :name",{'name':data.name}).first()
    spendingIndex = getBudgetSet(data.income,data.questionsSum)
    spending = db.query(SpendingType).filter(SpendingType.id == spendingIndex+2).first()
    userIndex = UserIncomeIndex(user=user.id,income=data.income,spendingType=spending.id)
    db.add(userIndex)
    db.commit()
    print(userIndex)
    return {'code':200,'message':'Budget calculated successfully','income':data.income,'RecommendedspendingSchema':budgetSets[spendingIndex]}
