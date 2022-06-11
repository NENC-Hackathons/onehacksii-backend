from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import CreateToken, CredentialsAreFree, CredentialsAreTrue
from database import User, session as db
from schemes import Token, CredentialSchema
from auth import context

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
        user = User(name=data.username,email=data.email,password=context.hash(data.password))
        try:
            db.add(user)
            db.commit()
        except:
            db.rollback()
        token = CreateToken(data.username)
        return {'code':200,'message':'User created successfully','token':token}
    return {'code':400,'message':'User already exists','token':None}

@app.post("/users/login")
async def login(data: CredentialSchema):
    if CredentialsAreTrue(data.username,data.password):
        token = CreateToken(data.username)
        return {'code':200,'message':'User logged in successfully','token':token}
    return {'code':401,'message':'Wrong Credentials','token':None}

@app.post("/users/{name}/devices")
async def devicesList(name: str, data: Token):
    return {'code':200,'message':'Devices list','devices':db.execute(f"SELECT * FROM devices WHERE user = :user",{'user':name})}