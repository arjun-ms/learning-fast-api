from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, auth
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from .routers import user

app = FastAPI()

# Include routers
app.include_router(user.router)

# Create the database tables
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#! Static Routes should be defined first before the Dynamic ones with path parameters.
#! This is to ensure that the Static routes are matched first before the Dynamic ones with path parameters.

# POST endpoint to create a new Todo
@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Todo, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Create a new Todo model instance with the data from the request
    new_todo = models.Todo(
        description=request.description,
        deadline=request.deadline,
        done=request.done,
        user_id=current_user.id  # Set the user_id to the current user's id
    )
       
    # Add the new Todo to the database
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo
# GET endpoint to retrieve all Todos
@app.get("/todo")
def get_all(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
    return todos

# Group todos by status (completed, pending, overdue)
@app.get("/todo/groups", status_code=status.HTTP_200_OK)
def group_todos(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Get all todos for the current user only
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).all()
    
    # Current time for comparing deadlines
    current_time = datetime.now()
    
    # Initialize result groups
    completed = []
    to_be_done = []
    time_elapsed = []
    
    # Categorize each todo
    for todo in todos:
        if todo.done:
            completed.append(todo)
        elif todo.deadline < current_time:
            time_elapsed.append(todo)
        else:
            to_be_done.append(todo)
    
    # Return grouped results
    return {
        "completed": completed,
        "to_be_done": to_be_done,
        "time_elapsed": time_elapsed
    }


# GET endpoint to retrieve a Todo by ID
@app.get("/todo/{id}", status_code=200)
def get_todo(id: int, response: Response, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todo = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id  
    ).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {id} not found")
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
def delete_todo(id, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Only delete if the todo belongs to the current user
    result = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id  
    ).delete(synchronize_session=False)
    
    if result == 0:  # No rows were deleted
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    db.commit()
    return f"Todo with {id} deleted successfully!"


# PUT endpoint to update a Todo by ID
@app.put("/todo/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(id, request: schemas.Todo, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todo_query = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id 
    )
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

# Mark todo as done
@app.put("/todo/{id}/mark-done", status_code=status.HTTP_202_ACCEPTED)
def mark_done(id, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    todo_query = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id 
    )
    todo = todo_query.first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    # Update the done status
    todo.done = True
    db.commit()
    
    return {"message": f"Todo with ID: {id} marked as done"}


