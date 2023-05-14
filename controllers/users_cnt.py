import bcrypt
from data import mysql_saver ,json_saver
from data.schemas.user import User
import logging
import uuid
from fastapi import HTTPException
from data.models.users import User as UserModel

class UsersCnt : 
    def __init__(self, title):
        self.title = title
        # self.data_setter = json_saver.JsonSaver('Users.json')
        self.data_setter = mysql_saver.MysqlSaverUser()

    def get_all(self):
        data = self.data_setter.find_all()
        logging.info("donnée recuperer")
        return data
    
    def add(self, user:User):
        logging.info("Usercnt: valeur index {index}")
        user.id = str(uuid.uuid4())
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password  =hashed_password.decode("utf-8")
        logging.info( user)
        self.data_setter.add(user.id,user.json())

    def delete(self, id:str):
        self.data_setter.delete(id)

    def get(self, id:str):
        return self.data_setter.find(id)
    

    def login(self, login_data):
        is_valid_email = self.data_setter.query(UserModel.email, login_data.login)
        is_valid_phone = self.data_setter.query(UserModel.phone, login_data.login)
        existuser:bool =False
        user
        if( len(is_valid_email) > 0 ):
            user = is_valid_email[0]
            existuser =True
        if(len(is_valid_phone)<= 0):
            user = is_valid_phone[0]
            existuser=True
        if (existuser == False):
            raise HTTPException(400, 'login ou mot de passe incorrect')
        if not self._verify_password(login_data.password, user.password):
            raise HTTPException(400, 'login ou mot de passe incorrect')


    def update(self, id:str, user:User):
        User.id = id
        return self.data_setter.update(id, user.json())
    
    def _verify_password(self,plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))