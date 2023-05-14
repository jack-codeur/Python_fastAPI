from sqlalchemy.orm import Session
from typing import List
import logging
import json

from sqlalchemy import Column
from data.models.users import User as UserModel
from data.schemas.todo import Todo, TodoCreate, TodoUpdate
from data.models.todos import Todo as TodoModel
from data.schemas.user import User, UserCreate, UserUpdate, UserDelete
from data.sql_database import SessionLocal, Base, engine

from sqlalchemy import create_engine



class MysqlSaver:
    def __init__(self):
        self.db:Session = SessionLocal()
        self.create_all(engine)
    
    def create_all(self, engine: create_engine):
        Base.metadata.create_all(bind=engine)
            

    def find_all(self) -> List[Todo]:
        return self.db.query(TodoModel).all()

    def find(self, todo_id: str) -> Todo:
        return self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()


    def add(self,id:str, todo_json: str) -> Todo:
        todo_create = TodoCreate.parse_raw(json.dumps(todo_json))
        todo = TodoModel(**todo_create.dict())
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def update(self, todo_id: str, todo_update_json: TodoUpdate) -> Todo:
        
        todo_update = TodoCreate.parse_raw(json.dumps(todo_update_json))
        db_todo = self.find(todo_id)
        if db_todo is None:
            logging.warning(f"Todo with id {todo_id} not found")
            return None
        for field, value in todo_update:
            setattr(db_todo, field, value)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def delete(self, todo_id: str):
        db_todo = self.find(todo_id)
        if db_todo is None:
            logging.warning(f"Todo with id {todo_id} not found")
            return None
        self.db.delete(db_todo)
        self.db.commit()



class MysqlSaverUser:
    def __init__(self):
        self.db:Session = SessionLocal()
        self.create_all(engine)
    
    def create_all(self, engine: create_engine):
        Base.metadata.create_all(bind=engine)
            

    def find_all(self) -> List[User]:
        return self.db.query(UserModel).all()

    def find(self, user_id: str) -> User:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()


    def query(self, field:Column, val:str):
        return self.db.query(UserModel).filter(field == val).all()

    def add(self,id:str, user_json: str) -> User:
        user_create = UserCreate.parse_raw(json.dumps(user_json))
        user = UserModel(**user_create.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: str, user_update_json: UserUpdate) -> User:
        
        user_update = UserCreate.parse_raw(json.dumps(user_update_json))
        db_user = self.find(user_id)
        if db_user is None:
            logging.warning(f"Todo with id {user_id} not found")
            return None
        for field, value in user_update:
            setattr(db_user, field, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: str):
        db_user = self.find(user_id)
        if db_user is None:
            logging.warning(f"user with id {user_id} not found")
            return None
        self.db.delete(db_user)
        self.db.commit()