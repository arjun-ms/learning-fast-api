## to start the app

```
uvicorn main:app --reload
```

`filename : the_variable_name` where you initialized the `FastAPI()`

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
