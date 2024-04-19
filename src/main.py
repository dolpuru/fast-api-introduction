from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id
from schema.request import CreateToDoRequest
from schema.response import ToDoSchema, ToDoListSchema

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
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db),
) -> ToDoListSchema:

    todos: List[ToDo] = get_todos(session=session)

    ret = list(todo_data.values())
    if order and order == "DESC":
        return ret[::-1]
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.id] = request.dict()



    return todo_data[request.id]

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int,
                        session: Session = Depends(get_db)):

    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return
    raise HTTPException(status_code=404, detail="ToDo Not Found")

@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int):
    todo = todo_data.get(todo_id)
    if todo:
        return
    raise HTTPException(status_code=404, detail="ToDo Not Found")


