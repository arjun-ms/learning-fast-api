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