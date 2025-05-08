from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, auth
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = utils.hash_password(user.password)
    
    # Create new user
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    
    # Add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # Verify user exists and password is correct
    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token (user's email is the payload/subject)
    access_token = auth.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}