from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlmodel import Session, select
from ..db import models
from .. import schemas, auth
from ..db.database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/todo",
    tags=["todos"]
)

# POST endpoint to create a new Todo
@router.post("", status_code=status.HTTP_201_CREATED)
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
@router.get("")
def get_all(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    statement = select(models.Todo).where(models.Todo.user_id == current_user.id)
    todos = db.exec(statement).all()
    return todos

# Group todos by status (completed, pending, overdue)
@router.get("/groups", status_code=status.HTTP_200_OK)
def group_todos(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Get all todos for the current user only
    statement = select(models.Todo).where(models.Todo.user_id == current_user.id)
    todos = db.exec(statement).all()
    
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
@router.get("/{id}", status_code=200)
def get_todo(id: int, response: Response, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == id, models.Todo.user_id == current_user.id)
    todo = db.exec(statement).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with ID {id} not found")
    return todo

# DELETE endpoint to delete a Todo by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == id, models.Todo.user_id == current_user.id)
    todo = db.exec(statement).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    db.delete(todo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# PUT endpoint to update a Todo by ID
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_todo(id: int, request: schemas.Todo, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == id, models.Todo.user_id == current_user.id)
    todo = db.exec(statement).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    # Update todo properties
    todo.description = request.description
    todo.deadline = request.deadline
    todo.done = request.done
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return {"message": f"Todo with id {id} updated successfully"}

# Mark todo as done
@router.put("/{id}/mark-done", status_code=status.HTTP_202_ACCEPTED)
def mark_done(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    statement = select(models.Todo).where(models.Todo.id == id, models.Todo.user_id == current_user.id)
    todo = db.exec(statement).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    
    # Update the done status
    todo.done = True
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return {"message": f"Todo with ID: {id} marked as done"}
