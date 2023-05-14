from sqlalchemy.orm import Session
from typing import List
import logging
from pydantic import BaseModel
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from sql_database import get_db, Base

from sqlalchemy import create_engine


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class SqlSaver:
    def __init__(self, model_type: type):
        self.model_type = model_type
        self.db:Session = get_db()

    @staticmethod
    def create_all(engine: create_engine, base: Base):
        if not engine.dialect.has_table(engine, base.__tablename__):
            base.metadata.create_all(bind=engine)

    def get_all(self) -> List[BaseModel]:
        return self.db.query(self.model_type).all()

    def get_by_id(self, id: str) -> BaseModel:
        return self.db.query(self.model_type).filter(self.model_type.id == id).first()

    def create(self, item_json: str) -> BaseModel:
        item_create = self.model_type.parse_raw(item_json)
        item = self.model_type.from_create(item_create)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, item_update: BaseModel) -> BaseModel:
        db_item = self.get_by_id(id)
        if db_item is None:
            logging.warning(f"{self.model_type.__name__} with id {id} not found")
            return None
        for field, value in item_update:
            setattr(db_item, field, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, id: str):
        db_item = self.get_by_id(id)
        if db_item is None:
            logging.warning(f"{self.model_type.__name__} with id {id} not found")
            return None
        self.db.delete(db_item)
        self.db.commit()