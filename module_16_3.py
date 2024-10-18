from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
async def get_all_users() -> dict:
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=3, description='User', example='Username')],
                   age: Annotated[int, Path(ge=18, le=99, example='18', description='Age')]) -> str:
    current_index = str(int(max(users, key=int)) + 1)
    users[current_index] = f'Имя: {username}, возраст: {age}'
    return f'User {username} created'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[str, Path(min_length=3)],
                      username: Annotated[str, Path(min_length=3, description='User', example='Username')],
                      age: Annotated[int, Path(ge=18, le=99, example='18', description='Age')]) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {username} updated'


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[str, Path(min_length=3)]) -> str:
    users.pop(user_id)
    return f'User ID={user_id} deleted'
