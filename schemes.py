from typing import List, Optional
from pydantic import BaseModel

class CredentialSchema(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class Token(BaseModel):
    token: str

class BudgetSchema(BaseModel):
    name: str
    income: float
    questions: List[int]