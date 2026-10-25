from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from database.database import get_db
from sqlalchemy.orm import Session
from database.model import Users, Restaurants, ResturantTables, Reservation
from security.security import check_access_token
from pydantic import BaseModel, Field
from typing import Literal

router = APIRouter(prefix="/reservation", tags=["Reservation"])

class ReservationCreate(BaseModel):
    table_no : int
    reservation_Date : str
    time_slot : str
    guest_count : int = Field(gt=0, description="Guest no should be greater than 0")
    status : Literal["booked", "cancelled"]

@router.post("/", status_code = 201)
def reserve_tables(data : ReservationCreate, db : Session = Depends(get_db), current_user : HTTPAuthorizationCredentials = Depends(check_access_token)):
    check_user = db.query(Users).filter(Users.id == current_user.id).first()
    if not check_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if check_user.role != "customer":
        raise HTTPException(status_code=403, detail="Unauthorized")
    check_table = db.query(ResturantTables).filter(ResturantTables.table_number == data.table_no).first()
    if not check_table:
        raise HTTPException(status_code=404, detail=f"table with id {data.table_no} not found")
    if check_table.table_capacity < data.guest_count:
        raise HTTPException(status_code=400, detail="Table capacity is less than no. of guest")
    check_reservation_duplication = db.query(Reservation).filter(Reservation.table_id == check_table.id, Reservation.reservation_date == data.reservation_Date.strip(), Reservation.time_slot == data.time_slot.strip(), Reservation.status == "booked").first()
    if check_reservation_duplication:
        raise HTTPException(status_code=409, detail=f"Table no. {data.table_no} is already booked on date {data.reservation_Date} {data.time_slot} by other customer")
    new_reservation = Reservation(customer_id = current_user.id, table_id = check_table.id, reservation_date = data.reservation_Date, time_slot = data.time_slot, guest_count = data.guest_count, status = data.status)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return {"Message" : "Table has been reserved succesfully", "Details" : new_reservation}

@router.get("/my")
def check_reservation(db : Session = Depends(get_db), current_user : HTTPAuthorizationCredentials = Depends(check_access_token)):
    check_user = db.query(Users).filter(Users.id == current_user.id).first()
    if not check_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    check_reservation = db.query(Reservation).filter(Reservation.customer_id == check_user.id).all()
    if not check_reservation:
        return {"Message" : "No reservation found"}
    return check_reservation

@router.post("/{reservation_id}/cancel")
def cancel_reservation(reservation_id : int, db : Session = Depends(get_db), current_user : HTTPAuthorizationCredentials = Depends(check_access_token)):
    check_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not check_reservation:
        raise HTTPException(status_code=404, detail="No reservation found")
    if check_reservation.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if check_reservation.status != "booked":
        raise HTTPException(status_code=400, detail="Reservation was already cancelled")
    check_reservation.status = "cancelled"
    db.commit()
    db.refresh(check_reservation)
    return {"Message" : "reservation has been cancelled succesfully", "Details" : check_reservation}