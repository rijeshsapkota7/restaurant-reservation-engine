from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Restaurants(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

class ResturantTables(Base):
    __tablename__ = "resturantTables"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    table_number = Column(Integer, nullable=False)
    table_capacity = Column(Integer, nullable=False)

    