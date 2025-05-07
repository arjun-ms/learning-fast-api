## to start the app

```
uvicorn todo.main:app --reload    
```

`module_or_folder_name.filename : the_variable_name` where you initialized the `FastAPI()`

---

### @app.get("/")
this means doing get **operation** on the **path** "/"
the function is called **path operation function** 
@app => **path operation decorator**


---

## Path Parameters
Path parameters allow you to capture dynamic values from the URL path. They are declared using curly braces {} in the route and become function arguments.

Syntax:
```
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

## Dynamic Routing
In FastAPI, when using dynamic routes, you should define them after static or more specific routes. Here's why:

FastAPI matches routes in the order they are defined.

Thumb Rule:
> Always place dynamic routes (with {}) after static or more specific routes.


## check for docs || we can also test there

http://localhost:8000/docs → 🚀 Swagger UI

http://localhost:8000/redoc → 📘 ReDoc UI (another doc UI FastAPI supports)

## Query Parameters

Query parameters are key-value pairs in the URL **after the `?`**, used to pass optional or filter-based data.

**URL Example:**

```
/items/?category=books&limit=10
```

**FastAPI Syntax:**

```python
@app.get("/items/")
def read_items(category: str = None, limit: int = 10, q: Optional[str] = None):
    return {"category": category, "limit": limit}
```

* Automatically parsed and validated by FastAPI.
* Can set **type** or set **default values** or make them **optional** with `= None` .
* We can use it for **filters**, **search terms**, and **pagination**.
* To make a parameter optional, assign a default value (e.g., None).
* Use Optional from typing for clarity (especially with type hints).
* FastAPI treats parameters with defaults as optional.

---

## Request Body

When you need to send data from a client (let's say, a browser) to your API, you send it as a request body.

To declare a request body, you use **Pydantic models**

## To Debug

- choose a line as **breakpoint**
- Press `Cntrl + Shift + P` => `Debug Restart` => Choose `FastAPI`

## To change PORT of running fastapi

add this line at the end:

```
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1", port=9000)
```

## ORMs

`Object Relational Mapping`

An ORM has tools to convert ("map") between **objects** in the code and **tables** ("relations") in a database.


You create a **class** that represents a **table** in the SQL DB.
Each **attribute** of the class represents a **column**, with a name and a type.

---

### 📦 Example with SQLAlchemy (used with FastAPI)

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
```

* `User` → represents the `users` table.
* `id`, `name`, `email` → columns in the table.
* The class lets you interact with SQL using **Python objects**, instead of raw SQL queries.

---

### 🧠 Benefits:

* Cleaner, readable code
* Safer queries (protects against SQL injection)
* Easy to switch databases with minimal changes

---

```
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
```

1. `create_engine(...)`

    Creates a connection engine for the SQLite database at ./todo.db.

2. `connect_args={"check_same_thread": False}`

    This is specific to SQLite. You need this line when using SQLite with FastAPI **to avoid threading errors.**

    SQLite is single-threaded -- By default, SQLite doesn't like it when different parts of your code (running at the same time) try to use the database.

    FastAPI is fast and async: It handles multiple things at the same time — this might confuse SQLite and cause errors.

    This setting (check_same_thread: False) tells SQLite:
        `“It’s okay if different threads use the database connection — don’t crash.”`
    
---

[TablePlus](https://tableplus.com) =>  Modern, Native and Friendly GUI Tool for Database Management

---

`database.py` -> This file contains the database connection and the `Base` class for the ORM models.

`models.py` -> This file defines the structure of the database table and its columns.  ( **Defines how data is stored (tables and columns).** )

`schemas.py` -> This file defines the shape of the data we accept or return in API. It is used for **Validating and serializing data**.  ( **Defines how data is validated when coming in or going out.** )

---

# FastAPI Endpoint Creation – Quick Notes

## 1. Define Endpoints with Functions

Each endpoint (like `/todo`, `/todo/{id}`) is tied to a function that:
- Accepts request data (optionally via Pydantic `schemas`)
- Interacts with the database using SQLAlchemy
- Returns a response (which FastAPI auto-converts to JSON)

---

## 2. Using `Depends(get_db)` to Access the Database

```python
db: Session = Depends(get_db)
```

`Depends()` is used for dependency injection

`get_db()` yields a SQLAlchemy session

# POST endpoint

```
@app.post("/todo", status_code=201)
def create(request: schemas.Todo, db: Session = Depends(get_db)):
    new_todo = models.Todo(
        description=request.description,
        deadline=request.deadline,
        done=request.done
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo
```
- Receives request body as a `schemas.Todo` object
- Creates a new` models.Todo` record
- Saves it to the database and returns the saved record

## Response Control

```python
from fastapi import Response

# Not recommended, but possible
response.status_code = status.HTTP_404_NOT_FOUND
return {"detail": "Not found"}
```

You can use `Response` to set status codes manually

But using `HTTPException` is much cleaner (one-liner).

## Summary Table

| Concept                 | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| `@app.post`, `@app.get` | Define API endpoints                         |
| `Depends(get_db)`       | Inject database session (dependency)         |
| `schemas.Todo`          | Validate incoming request data               |
| `models.Todo`           | Interact with the database via SQLAlchemy    |
| `HTTPException`         | Handle errors like "Not Found" or "Conflict" |


---

````markdown
## DELETE Endpoint: Two Approaches

### ✅ Method 1 – ORM Style (Safer)
```python
todo = db.query(models.Todo).filter(models.Todo.id == id).first()
if not todo:
    raise HTTPException(status_code=404)
db.delete(todo)
db.commit()
return Response(status_code=204)
````

* Checks if record exists (returns 404 if not)
* Uses `db.delete()` on ORM object
* Returns empty `204 No Content` response
* **Safer** and **more explicit**

---

### ⚡ Method 2 – Direct Query (Faster)

```python
db.query(models.Todo).filter(models.Todo.id == id).delete(synchronize_session=False)
db.commit()
return f"Todo with {id} deleted successfully!"
```

* Deletes directly using SQL query
* Skips existence check (may silently fail)
* Returns custom success message
* **Faster** but **less safe**

---

### Summary

**I have used the Faster Method**


| Method   | Safe? | Fast? | Handles 404? | Style       |
| -------- | ----- | ----- | ------------ | ----------- |
| Method 1 | ✅     | ❌     | ✅            | ORM-based   |
| Method 2 | ❌     | ✅     | ❌            | Query-based |

```

---

```
def update_todo(id, request: schemas.Todo, db: Session = Depends(get_db)):
```

#### Q: What is the need for these two params : 
`request: schemas.Todo`, `db: Session = Depends(get_db)` 

1. `request: schemas.Todo`
    Validates and parses incoming JSON data.
    This means the request body should match the structure defined in schemas.Todo (like description, deadline, done)

2. `db: Session = Depends(get_db)`
    Provides a DB connection for queries.
    This gives you a database session for the request
        1. Runs the get_db() function
        2. Connects to DB at the start
        3. Closes the DB after the request finishes

---

### using postgres instead of sqllite

get a connection string of your local postgres instance:

```
postgresql://<username>:<password>@<host>:<port>/<database>
```

Avoid hardcoding this in your codebase. Use environment variables instead.