from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

class Reservations(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    arrival_date = Column(DateTime())
    departure_date = Column(DateTime())
