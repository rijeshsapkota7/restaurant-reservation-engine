from security.security import hash_password
from database.model import Users
from database.database import LocalSession
from security.env_loader import ADMIN_EMAIL, ADMIN_PSWD

def create_super_admin():
    email = ADMIN_EMAIL
    password = hash_password(ADMIN_PSWD)
    db = LocalSession()
    chec_duplication = db.query(Users).filter(Users.email == email).first()
    if not chec_duplication:
            admin = Users(name="System Adminstator", email=email, password = password, role="admin")
            db.add(admin)
            db.commit()