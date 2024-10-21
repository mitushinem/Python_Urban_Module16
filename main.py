# from xml.sax import parse
#
# from fastapi import FastAPI, Path
# from typing import Annotated
#
# app = FastAPI()

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


# messages_db = {'0': 'First post in FastAPI'}
#
#
# @app.get('/')
# async def get_all_messages() -> dict:
#     return messages_db
#
#
# @app.get('/message/{message_id}')
# async def get_all_messages(message_id: str) -> dict:
#     return messages_db[message_id]
#
#
# @app.post('/message')
# async def create_message(message: str) -> str:
#     current_index = str(int(max(messages_db, key=int)) + 1)
#     messages_db[current_index] = message
#     return 'Message created'
#
#
# @app.put('/message/{message_id}')
# async def update_message(message_id: str, message: str) -> str:
#     messages_db[message_id] = message
#     return 'Message updated'
#
#
# @app.delete('/message/{message_id}')
# async def delete_message(message_id: str) -> str:
#     messages_db.pop(message_id)
#     return f'Message {message_id} deleted'
#
#
# @app.delete('/')
# async def delete_all_messages() -> str:
#     messages_db.clear()
#     return 'All messages deleted'




from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

messages_db = []


class Message(BaseModel):
    id: int = None
    text: str


@app.get("/")
def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("message.html", {"request": request, "messages": messages_db})


@app.get(path="/message/{message_id}")
def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("message.html", {"request": request, "message": messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/", status_code=status.HTTP_201_CREATED)
def create_message(request: Request, message: str = Form()) -> HTMLResponse:
    if messages_db:
        message_id = max(messages_db, key=lambda m: m.id).id + 1
    else:
        message_id = 0
    messages_db.append(Message(id = message_id, text = message))
    return templates.TemplateResponse("message.html", {"request": request, "message": messages_db})


@app.put("/message/{message_id}")
def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return f"Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/message/{message_id}")
def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/")
def kill_message_all() -> str:
    messages_db.clear()
    return "All messages deleted!"