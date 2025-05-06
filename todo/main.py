from fastapi import FastAPI,Depends
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/todo")
def create(request: schemas.Todo, db: Session = Depends(get_db)):
    return db
