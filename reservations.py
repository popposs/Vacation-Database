from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True)
    name = Column(String(256))
    arrival_date = Column(DateTime())
    departure_date = Column(DateTime())
