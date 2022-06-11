from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import session as db

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