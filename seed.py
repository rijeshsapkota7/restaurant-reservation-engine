from security.security import hash_password
from database.model import Users
from database.database import LocalSession

def create_super_admin():
    email = "admin@gmail.com"
    password = hash_password("Admin")
    db = LocalSession()
    chec_duplication = db.query(Users).filter(Users.email == email).first()
    if not chec_duplication:
            admin = Users(name="System Adminstator", email=email, password = password, role="admin")
            db.add(admin)
            db.commit()