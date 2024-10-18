from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def index() -> str:
    return 'Главная страница'


@app.get('/user/admin')
async def index_admin() -> str:
    return 'Вы вошли как администратор'


@app.get('/user/{user_id}')
async def index_user(user_id: str) -> str:
    return f'Вы вошли как пользователь № {user_id}'


@app.get('/user')
async def user_info(username: str, age: int) -> str:
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'
