from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping" : "pong"}

todo_data = {
    1: {
        "id": 1,
        "contents": "실전! FastAPI 섹션 0 수강",
        "is-done": True,
    },


    2: {
        "id": 2,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is-done": True,
    },


    3: {
        "id": 3,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is-done": True,
    },
}

@app.get("/todos", status_code=200)
def get_todos_handler(order: str | None = None):
    ret = list(todo_data.values())
    if order and order == "DESC":
        return ret[::-1]
    return ret

class CreateToDoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

@app.post("/todos")
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]

@app.delete("/todos/{todo_id}", status_code=200)
def delete_todo_handler(todo_id: int):
    todo = todo_data.get(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found")

    todo_data.pop(todo_id, None)
    return todo_data

@app.get("/todos/{todo_id}")
def get_todo_handler(todo_id: int):
    return todo_data.get(todo_id, {})

