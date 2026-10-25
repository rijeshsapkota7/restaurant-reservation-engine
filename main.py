from fastapi import FastAPI
from seed import create_super_admin
from database.database import Base, engine
from database.model import Users, Restaurants, ResturantTables, Reservation
from routers import users, restaurants, reservation

Base.metadata.create_all(bind=engine)
create_super_admin()
app = FastAPI(title="Restaurant Reservation Engine")


app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(reservation.router)

@app.get("/")
def home():
    return {"Status" : "online", "Service" : "Reservation engine"}