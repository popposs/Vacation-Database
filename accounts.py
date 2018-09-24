from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True)
    name = Column(String(256))
