from sqlalchemy import Column, Integer, String
from .base import BaseModel
from sqlalchemy.orm import relationship

class Seller(BaseModel):
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    books = relationship("Book", back_populates="seller")