from sqlalchemy import Column, Integer, String, Boolean
from data.sql_database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(255), primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), index=True, unique=True)
    phone = Column(String(255), index=True, unique=True)
    password = Column(String(255))