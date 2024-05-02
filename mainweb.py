from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from db import update_data, create_table, get_connection, add_data, login_data, delete_data1


app=FastAPI()


@app.get('/')
def read_root(data):
    print(data)
    return {"Welcome": "Gulam Sarvar"}


@app.get("/get_coonection")
async def get_connection():
    conn = get_connection()
    return {"message": "Connection successful"}


@app.get("/create_table")
async def create_table():
    create_table()
    return {"message": "Table created successfully"}


@app.post("/add_data")
async def add_values(id: int, name: str, username: str, password: str):
    query = "INSERT INTO login (id,name, username,password) VALUES (%s, %s, %s, %s);"
    params = (id, name, username, password)
    if add_data(query, params):
        return {"message": "Values added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to add values")



@app.get("/print_data")
async def print_data(username: str):
    query = "SELECT * FROM login where username = %s;"
    params = (username)
    value=print_data(query)
    if print_data(query):
        return {"message": "Data printed successfully {value}"}
    else:
        return {"message": "Failed to print data"}


@app.put("/update_data")
async def update_database(id: int, name: str):
    query = "UPDATE login SET name = %s WHERE id = %s;"
    params = (name, id)
    if update_data(query, params):
        return {"message": "Data updated successfully"}
    else:
        return {"message": "Failed to update data"}
    

@app.post("/login_data")
async def login_page(username: str, password: str):
    is_authenticated = await login_data(username, password)
    if is_authenticated:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")



@app.delete("/delete_data")
async def delete_data(id: int):
    query = "DELETE FROM login WHERE id = %s;"
    params = (id,)
    if delete_data1(query,params):
        return {"message": "Data deleted successfully"}
    else:
        return {"message": "Failed to delete data"}
    

