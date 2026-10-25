from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from database.database import get_db
from sqlalchemy.orm import Session
from database.model import Users, Restaurants, ResturantTables
from security.security import check_access_token
from pydantic import BaseModel

class CreateRestaurant(BaseModel):
    name : str
    city : str
    address : str

class CreateReastaurantTable(BaseModel):
    table_number : int
    table_capacity : int

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/", status_code=201)
def create_restaurants(data : CreateRestaurant, db : Session = Depends(get_db), current_user : HTTPAuthorizationCredentials = Depends(check_access_token)):
    check_user = db.query(Users).filter(Users.id == current_user.id).first()
    if not check_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if check_user.role != "owner":
        raise HTTPException(status_code=403, detail="Not authorized")
    check_restaurant_duplication = db.query(Restaurants).filter(Restaurants.name.ilike(data.name), Restaurants.city.ilike(data.city)).first()
    if check_restaurant_duplication:
        raise HTTPException(status_code=403, detail="Restaurant with this name is already available in this city")
    new_restaurant = Restaurants(name=data.name, city=data.city, address=data.address, owner_id=check_user.id)
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return {"Message" : "Restaurant registered Successfully", "Details" : new_restaurant}

@router.get("/")
def search_restaurants(city : str = None, db : Session = Depends(get_db)):
    if city is None:
        all_restaurants = db.query(Restaurants).all()
    else:
        all_restaurants = db.query(Restaurants).filter(Restaurants.city.ilike(city)).all()
    return all_restaurants


@router.post("/{restaurant_id}/tables", status_code=201)
def create_table(restaurant_id : int, data : CreateReastaurantTable, db : Session = Depends(get_db), current_user : HTTPAuthorizationCredentials = Depends(check_access_token)):
    check_user = db.query(Users).filter(Users.id == current_user.id).first()
    if not check_user:
        raise HTTPException(status_code=403, detail="Not authenticated")
    check_reasturant = db.query(Restaurants).filter(Restaurants.id == restaurant_id).first()
    if check_user.id !=   check_reasturant.owner_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    check_table = db.query(ResturantTables).filter(ResturantTables.table_number == data.table_number).first()
    if check_table:
        raise HTTPException(status_code=409, detail=f"Table with the number {data.table_number} already exists")
    new_table = ResturantTables(restaurant_id=restaurant_id, table_number = data.table_number, table_capacity = data.table_capacity)
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return {"Message" : "Table created successfully", "details" : new_table}

@router.get("/{restaurant_id}/tables")
def search_tables(restaurant_id : int, min_capacity : int = None, db : Session = Depends(get_db)):
    check_restaurant = db.query(Restaurants).filter(Restaurants.id == restaurant_id).first()
    if not check_restaurant:
        raise HTTPException(status_code=404, detail=f"Restaurant with id {restaurant_id} not found")
    if min_capacity is None:
        all_tables = db.query(ResturantTables).filter(ResturantTables.restaurant_id == restaurant_id).all()
    else:
        all_tables = db.query(ResturantTables).filter(ResturantTables.restaurant_id == restaurant_id, ResturantTables.table_capacity >= min_capacity).all()
    return all_tables