# This file defines the SQLAlchemy ORM model for the todo application.
# It uses SQLAlchemy to define the structure of the database table and its columns.
from sqlalchemy import Column, Integer, String
from .database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    done = Column(bool, default=False)