from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def welome() -> dict:
    return {"message": "Hello World"}

@app.get("/user/A/B")
def news() -> dict:
    return {"message": f"Hello Tester!"}

@app.get("/user/{first_name}/{last_name}")
async def news(first_name: str, last_name: str) -> dict:
    return {"message": f"Hello {first_name} {last_name}"}


@app.get("/id")
async def id_paginator(username: str, age: int) -> dict:
    return {"User": username, "Age": age}

