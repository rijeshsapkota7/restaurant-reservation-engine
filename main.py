from fastapi import FastAPI
from seed import create_super_admin
from database.database import Base, engine
from database.model import Users, Restaurants, ResturantTables
from routers import users, restaurants

Base.metadata.create_all(bind=engine)
create_super_admin()
app = FastAPI(title="Restaurant Reservation Engine")


app.include_router(users.router)
app.include_router(restaurants.router)

@app.get("/")
def home():
    return {"Status" : "online", "Service" : "Reservation engine"}