from datetime import timedelta,datetime
from jose import jwt
from passlib.context import CryptContext
from config import secret

context = CryptContext(schemes=["bcrypt"], deprecated="auto")