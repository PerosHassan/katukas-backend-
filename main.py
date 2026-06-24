import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model Table
class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Katukas Kitchen API")

# Data structures for incoming API requests
class MenuItemCreate(BaseModel):
    name: str
    description: str = None
    price: float
    is_available: bool = True

class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    is_available: bool

    class Config:
        from_attributes = True

# Database Helper Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Katukas Kitchen Live DB!"}

# POST endpoint to create a new food item
@app.post("/menu/", response_model=MenuItemResponse)
def create_menu_item(item: MenuItemCreate, db: Session = Depends(get_db)):
    db_item = MenuItem(
        name=item.name,
        description=item.description,
        price=item.price,
        is_available=item.is_available
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# GET endpoint to fetch all food items
@app.get("/menu/", response_model=List[MenuItemResponse])
def get_all_menu_items(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()
