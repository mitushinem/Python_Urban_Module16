from xml.sax import parse

from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

# @app.get("/")
# async def welome() -> dict:
#     return {"message": "Hello World"}
#
# @app.get("/user/A/B")
# def news() -> dict:
#     return {"message": f"Hello Tester!"}
#
# @app.get("/user/{username}/{id}")
# async def news(username: Annotated[str, Path(min_length=3, max_length=15, description='Enter username', example='montes')],
#                id: Annotated[int, Path(ge=0, le=100, description='Enter your id', example='75')]) -> dict:
#     return {"message": f"Hello {username}:{id}"}
#
#
# @app.get("/id")
# async def id_paginator(username: str, age: int) -> dict:
#     return {"User": username, "Age": age}


messages_db = {'0': 'First post in FastAPI'}


@app.get('/')
async def get_all_messages() -> dict:
    return messages_db


@app.get('/message/{message_id}')
async def get_all_messages(message_id: str) -> dict:
    return messages_db[message_id]


@app.post('/message')
async def create_message(message: str) -> str:
    current_index = str(int(max(messages_db, key=int)) + 1)
    messages_db[current_index] = message
    return 'Message created'


@app.put('/message/{message_id}')
async def update_message(message_id: str, message: str) -> str:
    messages_db[message_id] = message
    return 'Message updated'


@app.delete('/message/{message_id}')
async def delete_message(message_id: str) -> str:
    messages_db.pop(message_id)
    return f'Message {message_id} deleted'


@app.delete('/')
async def delete_all_messages() -> str:
    messages_db.clear()
    return 'All messages deleted'
