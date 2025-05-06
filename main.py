# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional

# app = FastAPI()

# class Todo(BaseModel):
#     id: int
#     description: str
#     done: bool = False

# @app.get("/")
# def hello_world():
#     return "Hello, Arjun!"

# @app.get("/todo/{id}")
# def show():
#     pass

# @app.post("/todo")
# def create_todo(todo: Todo):
#     return {"data": f"Todo with id {todo.id} created successfully!"}