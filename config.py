from os import environ
from dotenv import load_dotenv

load_dotenv()
url = environ.get('DATABASE_URL')
secret = environ.get('SECRET')