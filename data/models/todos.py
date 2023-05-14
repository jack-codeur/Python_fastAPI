from sqlalchemy import Column, Integer, String, Boolean
from data.sql_database import Base

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(String(255), primary_key=True, index=True)
    title = Column(String(255))
    content = Column(String(255))
    completed = Column(Boolean, default=False)
