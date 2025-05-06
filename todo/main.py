from fastapi import FastAPI,Depends,status, Response, HTTPException
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
@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Todo, db: Session = Depends(get_db)):
    # Create a new Todo model instance with the data from the request
    new_todo = models.Todo(
        description=request.description,
        deadline=request.deadline,
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
@app.get("/todo/{id}", status_code=200)
def get_todo(id: int,response:Response, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Todo with {id} not found"}
    return todo

# DELETE endpoint to fetch and then delete a Todo by ID (Safer but slower approach -- 2 DB calls)
# @app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_todo(id,db: Session = Depends(get_db)):
#     todo = db.query(models.Todo).filter(models.Todo.id == id).first()
#     if not todo:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with {id} not found")
#     db.delete(todo)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# DELETE endpoint to delete a Todo by ID (Slightly faster — one DB call, but less safe)
# This approach is less safe because it doesn't check if the Todo exists before deleting it.
@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id,db: Session = Depends(get_db)):
    db.query(models.Todo).filter(models.Todo.id == id).delete(synchronize_session=False)
    db.commit()
    return f"Todo with {id} deleted successfully!"


# PUT endpoint to update a Todo by ID
@app.put("/todo/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(id, request: schemas.Todo, db: Session = Depends(get_db)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == id)
    todo = todo_query.first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    # Update with a dictionary of values
    update_data = {
        "description": request.description,
        "deadline": request.deadline,
        "done": request.done
    }
    
    todo_query.update(update_data, synchronize_session=False)
    db.commit()
    
    return {"message": f"Todo with id {id} updated successfully"}