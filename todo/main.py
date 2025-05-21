from fastapi import FastAPI

from .db import models
from .db.database import engine, create_db_and_tables
from .routers import user, todos,chat

app = FastAPI()

# Include routers
app.include_router(user.router)
app.include_router(todos.router)
app.include_router(chat.router) #! implemented for chat app on websockets

# Create the database tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


