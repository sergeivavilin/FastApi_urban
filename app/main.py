import uvicorn
from fastapi import FastAPI
from routers.user import user_router
from routers.task import task_router


app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(user_router)
app.include_router(task_router)


if __name__ == '__main__':
    uvicorn.run(app)
