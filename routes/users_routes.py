from typing import Dict, List, Union
from controllers.users_cnt import UsersCnt
from data.schemas.user import User, UserCreate, UserDelete, UserUpdate
from fastapi import APIRouter
router = APIRouter()

users_cnt = UsersCnt("User controller")

@router.get('/users/',tags=["users"], summary="get all users")
def get_users():
    return users_cnt.get_all()

@router.get('/users/{id}',tags=["users"], summary="get a user")
def get_user(id:str):
    return users_cnt.get(id)

@router.post('/users/',tags=["users"], summary="add a user")
def add_users(user: UserCreate):
    return users_cnt.add(user)

@router.put('/users/{id}',tags=["users"], summary="update a user")
def update_users(id:str, user: UserUpdate):
    return users_cnt.update(id,user)

@router.delete('/users/{id}',tags=["users"], summary="delete a user")
def delete_user(id:str):
    return users_cnt.delete(id)