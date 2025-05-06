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


# POST endpoint to create a new Todo
@app.post("/todo")
def create(request: schemas.Todo, db: Session = Depends(get_db)):
    # Create a new Todo model instance with the data from the request
    new_todo = models.Todo(
        description=request.description,
        done=request.done)
       
    # Add the new Todo to the database
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

# GET endpoint to retrieve all Todos
@app.get("/todo")
def get_all(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos

# GET endpoint to retrieve a Todo by ID
@app.get("/todo/{id}")
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        return {"error": "Todo not found"}
    return todo