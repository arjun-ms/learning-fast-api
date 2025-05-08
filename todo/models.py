# This file defines the SQLAlchemy ORM model for the todo application.
# It uses SQLAlchemy to define the structure of the database table and its columns.
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    deadline = Column(DateTime)
    done = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)