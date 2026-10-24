from fastapi import FastAPI
from seed import create_super_admin
from database.database import Base, engine
from database.model import Users
from routers import users

app = FastAPI(title="Restaurant Reservation Engine")

Base.metadata.create_all(engine)

create_super_admin()

app.include_router(users.router)


@app.get("/")
def home():
    return {"Status" : "online", "Service" : "Reservation engine"}