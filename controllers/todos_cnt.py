from data import mysql_saver ,json_saver
from data.schemas.todo import Todo
import logging
import uuid

class TodosCnt : 
    def __init__(self, title):
        self.title = title
        # self.data_setter = json_saver.JsonSaver('todos.json')
        self.data_setter = mysql_saver.MysqlSaver()

    def get_all(self):
        data = self.data_setter.find_all()
        logging.info("donnée recuperer")
        return data
    
    def add(self, todo:Todo):
        logging.info("todocnt: valeur index {index}")
        todo.id = str(uuid.uuid4())
        todo.completed = False
        self.data_setter.add(todo.id,todo.json())

    def delete(self, id:str):
        self.data_setter.delete(id)

    def get(self, id:str):
        return self.data_setter.find(id)
    
    def update(self, id:str, todo:Todo):
        todo.id = id
        return self.data_setter.update(id, todo.json())