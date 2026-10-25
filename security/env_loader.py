import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:////tmp/reservations.db"
SECREATKEY = os.getenv("SECRET_KEY") or "ThisIsTheFirstSecurityKeyOfMyProgram"
ALGORITHM = os.getenv("ALGORITHM") or "HS256"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL") or "admin@gmail.com"
ADMIN_PSWD = os.getenv("ADMIN_PASSWORD") or "Admin"