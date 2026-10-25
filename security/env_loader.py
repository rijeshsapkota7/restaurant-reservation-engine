import os
from dotenv import load_dotenv

load_dotenv()

SQLITEURL = os.getenv("DATABASE_URL")
SECREATKEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PSWD = os.getenv("ADMIN_PASSWORD")