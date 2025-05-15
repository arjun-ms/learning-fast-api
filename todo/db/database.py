# This file contains the database connection for SQLModel.
from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "makemypass")

# Construct database URL from environment variables
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# For SQLite database
# DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL)

# Dependency
def get_db():
    with Session(engine) as session:
        yield session

# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
