from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from slugify import slugify

from backend.db_depends import get_db
from models import Task, User
from schemas import CreateTask, UpdateTask


task_router = APIRouter(prefix="/task", tags=["task"])

@task_router.get("/")
async def all_tasks(get_db_session: Annotated[Session, Depends(get_db)]):
    get_all_tasks = get_db_session.scalars(select(Task)).all()
    return get_all_tasks


@task_router.get("/task/{id}")
async def task_by_id(get_db_session: Annotated[Session, Depends(get_db)], task_id: int):
    task = get_db_session.scalar(select(Task).where(Task.id == task_id))

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    return task


@task_router.post("/create")
async def create_task(get_db_session: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user = get_db_session.scalars(select(User).where(User.id == user_id)).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    get_db_session.execute(insert(Task).values(title=create_task.title,
                                               content=create_task.content,
                                               priority=create_task.priority,
                                               user_id=create_task.user_id,
                                               slug=slugify(create_task.title)
                                               )
                           )
    get_db_session.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@task_router.put("/update")
async def update_task(get_db_session: Annotated[Session, Depends(get_db)], update_task: UpdateTask, user_id: int):
    user = get_db_session.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    get_db_session.execute(update(Task).where(Task.user_id.id == user_id).values(title=update_task.title,
                                                                                 content=update_task.content,
                                                                                 priority=update_task.priority,
                                                                                 slug=slugify(update_task.title)
                                                                                 )
                           )
    get_db_session.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}


@task_router.delete("/delete")
async def delete_task(get_db_session: Annotated[Session, Depends(get_db)], task_id: int):
    task = get_db_session.scalar(select(Task).where(Task.id == task_id))

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    get_db_session.execute(delete(Task).where(Task.id == task_id))
    get_db_session.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}

