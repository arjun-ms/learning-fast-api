# this file contains the schemas for the todo application
# and is used to define the data models for the application.
from pydantic import BaseModel

class Todo(BaseModel):
    description: str
    done: bool