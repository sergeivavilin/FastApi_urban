from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from slugify import slugify

from backend.db_depends import get_db
from models import User
from schemas import CreateUser, UpdateUser


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/")
async def all_users(get_db_session: Annotated[Session, Depends(get_db)]):
    get_all_users = get_db_session.scalars(select(User)).all()
    return get_all_users


@user_router.get("/user_id")
async def user_by_id(get_db_session: Annotated[Session, Depends(get_db)], user_id: int):
    user = get_db_session.scalars(select(User).where(User.id == user_id)).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user


@user_router.post("/create")
async def create_user(get_db_session: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    user = get_db_session.scalar(select(User).where(User.username == create_user.username))

    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exists")

    get_db_session.execute(insert(User).values(username=create_user.username,
                                               firstname=create_user.firstname,
                                               lastname=create_user.lastname,
                                               age=create_user.age,
                                               slug=slugify(create_user.username)
                                               )
                           )
    get_db_session.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@user_router.put("/update")
async def update_user(get_db_session: Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: int):
    user = get_db_session.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    get_db_session.execute(update(User).where(User.id == user_id).values(firstname=update_user.firstname,
                                                                         lastname=update_user.lastname,
                                                                         age=update_user.age,
                                                                         )
                           )
    get_db_session.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@user_router.delete("/delete")
async def delete_user(get_db_session: Annotated[Session, Depends(get_db)], user_id: int):
    user = get_db_session.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    get_db_session.execute(delete(User).where(User.id == user_id))
    get_db_session.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
