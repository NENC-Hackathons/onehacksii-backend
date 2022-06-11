from typing import Optional
from pydantic import BaseModel

class CredentialSchema(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class Token(BaseModel):
    token: str