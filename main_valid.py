from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import uuid
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import psycopg2
import bcrypt

# Pydantic model for user login
class userlogin(BaseModel):
    email: str
    password: str

# Pydantic model for user registration
class user(BaseModel):
    email: str
    username: str
    password: str

app=FastAPI()

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
            CREATE TABLE users (
            public_id UUID PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR NOT NULL);
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


SECRET_KEY='d6d2e8a428b9ea5e7856e66f736dd74de2c8979fe38daa00dc3a9280c116a3e8'

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate JWT token
def create_token(public_id: str):
    token = jwt.encode({
        'public_id': public_id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, SECRET_KEY)
    return token


@app.post('/add_data')
def add_data(email: str,username: str, password: str):
    data=user(email=email,username=username, password=password)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid user data")
    else:
        db_conn=get_connection()
        db_cursor=db_conn.cursor()
    try:
        # Check if user already exists
        db_cursor.execute("SELECT * FROM users WHERE email = %s ", (data.email,))
        existing_user = db_cursor.fetchone()
        if existing_user:
            db_conn.close()
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash password
        hashed_password = pwd_context.hash(data.password)
        # pwd_bytes = password.encode('utf-8')
        # salt = bcrypt.gensalt()
        # hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)

        # Generate public id
        public_id = str(uuid.uuid4())

        # Insert new user
        db_cursor.execute("INSERT INTO users (public_id,  email, username, password) VALUES (%s , %s, %s, %s)",
                (public_id, data.email, data.username, hashed_password))
        db_conn.commit()
        db_conn.close()
        db_cursor.close()
        return {"message": "User registered successfully"}
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        return {"message": "Error while registering user"}  
    return {"message": "User registered successfully"}


@app.post('/login')
def login(email: str, password: str):
    data=userlogin(email=email, password=password)
    db_conn=get_connection()
    db_cursor=db_conn.cursor()
    try:
        # Check if user exists
        db_cursor.execute("SELECT * FROM users WHERE email = %s ", (data.email,))
        user = db_cursor.fetchone()
        if not user:
            db_conn.close() 
            raise HTTPException(status_code=400, detail="User does not exist")  
        # Check if password is correct
        # hashed=user[2].encode('utf-8')
        if not pwd_context.verify(password, user[3]):
            db_conn.close()
            raise HTTPException(status_code=400, detail="Incorrect password")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        return {"message": "some error occured"}
    finally:
        db_conn.close()
        db_cursor.close()

    jwt_token=create_token(user[0])
    return print("message User logged in successfully", jwt_token)


# @app.get('/user')
# def get_user(token: str = Depends(oauth2_scheme)):
#     user_id = decode_token(token)
#     db_conn=get_connection()
#     db_cursor=db_conn.cursor()
#     try:
#         db_cursor.execute("SELECT * FROM users WHERE public_id = %s ", (user_id,))
#         user = db_cursor.fetchone()
#         if not user:
#             db_conn.close() 
#             raise HTTPException(status_code=400, detail="User does not exist")  
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Error while connecting to PostgreSQL", error)
#         return {"message": "some error occured"}
#     finally:
#         db_conn.close()
#         db_cursor.close()   
#         return {"message": "User logged in successfully", "user": user}



# https://medium.com/@chnarsimha986/fastapi-login-logout-changepassword-4c12e92d41e2


