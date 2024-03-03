from pydantic import BaseModel, EmailStr
from typing import List
from .books import ReturnedBook  # Импортируем схему книги

class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class SellerCreate(BaseSeller):
    password: str

class Seller(BaseSeller):
    id: int

    class Config:
        orm_mode = True

class SellerDetail(BaseSeller):
    id: int
    books: List[ReturnedBook] = []  # ReturnedBook для списка книг

    class Config:
        orm_mode = True
