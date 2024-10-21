from fastapi import (
    FastAPI,
    Path,
    HTTPException,
    Request
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from pydantic import BaseModel


app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/user/{user_id}')
async def get_all_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id]})


@app.post('/user/{username}/{age}')
async def post_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(le=120, ge=18, description='Enter age', example='24')]
) -> User:
    user_id = max(users, key=lambda x: int(x.id)).id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
        username: Annotated[str, Path(min_length=5, max_length=20,
                                      description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(le=120, ge=18, description='Enter age', example='24')]
) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> str:
    for i in range(len(users)):
        if users[i].id == user_id:
            del users[i]
            return f'User ID={user_id} deleted'
    raise HTTPException(status_code=404, detail='User was not found')
