from fastapi import FastAPI

from .db import models
from .db.database import engine, create_db_and_tables
from .routers import user, todos

app = FastAPI()

# Include routers
app.include_router(user.router)
app.include_router(todos.router)

# Create the database tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


