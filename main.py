from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import psycopg2
app=FastAPI()

class user(BaseModel):
    id: int
    email: EmailStr
    username: str
    password: str

@app.get('/')
def read_root(data):
    print(data)
    return {"Welcome": "Gulam Sarvar"}

def get_connection():
    try:
        db_conn = psycopg2.connect(
            dbname="BlueBash",
            user="postgres",
            password="7895",
            host="127.0.0.1",
            port="5432"
        )
        print("Connection to PostgreSQL successful!")
        return db_conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

    
@app.post('/create_table')
def create_table():
    try:
        db_conn = get_connection()
        if db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS userdata (
                id SERIAL PRIMARY KEY,
                email VARCHAR(100),
                username VARCHAR(100) UNIQUE,
                password VARCHAR(100)
            );
            """)
            db_conn.commit()
            db_cursor.close()
            db_conn.close()
            print("Table created successfully!")
        else:
            print("Failed to create table. No database connection.")
    except Exception as e:
        print("Error while creating table:", e)
    return "Table created successfully"


@app.post('/add_data')
def add_data(id: int, username: str, email: str, password: str):
    data=user(id=id, username=username, email=email, password=password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user data")
    else:
        db_conn=get_connection()
        db_cursor=db_conn.cursor()
    try:
        db_cursor.execute('insert into userdata (id, username, email, password) values (%s, %s, %s, %s)',
                              (data.id, data.username, data.email,data.password))
        db_conn.commit()
    except psycopg2.Error as e:
        # db_conn.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        db_cursor.close()
    return {"message": "User created successfully"}


@app.post('/login')
def login(email: str, password: str):
        # data=user(email=email, password=password)
        db_conn=get_connection()
        if db_conn:
            db_cursor=db_conn.cursor()
            try:
                db_cursor.execute("select * from userdata where email=%s and password=%s",(email, password))
                user_data = db_cursor.fetchone()
                if user_data:
                    return {"message": "Login successful"}
            except:
                 raise HTTPException(status_code=401, detail="Invalid username or password")
            finally:
                db_conn.close()
                db_cursor.close()
        else:
            print("Error while connecting to Database")
        return {"login complete"}


@app.delete('/delete_user_data')
def delete_data(id: int):
    # data=user(id=Id)
    db_conn=get_connection()
    if db_conn:
        db_cursor=db_conn.cursor()
        try:
            db_cursor.execute("delete from userdata where id=%s",(id,))
            db_conn.commit()
        except:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        finally:
                db_conn.close()
                db_cursor.close()
    else:
        print("Error while connecting to Database")
    return {"message": "User deleted successfully"}
    

@app.put('/update_data')
def update_data(id: int, username: str):
    # data=user(id=id, username=username)
    db_conn=get_connection()
    if db_conn:
        db_cursor=db_conn.cursor()
        try:
            db_cursor.execute("update userdata set username=%s where id=%s",(username, id)) 
            db_conn.commit()
        except:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        finally:
                db_conn.close()
                db_cursor.close()
    else:
        print("Error while connecting to Database")
    return {"message": "User updated successfully"}


