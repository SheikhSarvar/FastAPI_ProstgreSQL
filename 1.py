from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import psycopg2

# Pydantic model for user login
class UserLogin(BaseModel):
    email: str
    password: str

# Pydantic model for user registration
class User(BaseModel):
    name: str
    email: str
    password: str

# FastAPI app instance
app = FastAPI()

# Database connection configuration
DATABASE_NAME = "BlueBash"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "7895"
DATABASE_HOST = "127.0.0.1"
DATABASE_PORT = "5432"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate JWT token
SECRET_KEY = 'd6d2e8a428b9ea5e7856e66f736dd74de2c8979fe38daa00dc3a9280c116a3e8'

def create_token(public_id: str):
    token = jwt.encode({
        'public_id': public_id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, SECRET_KEY)
    return token

# Database connection function
def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        print("Connection to PostgreSQL successful!")
        return conn
    except psycopg2.Error as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

# Create table endpoint
@app.post('/create_table')
def create_table():
    try:
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                public_id VARCHAR(50) UNIQUE,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                password VARCHAR(100)
            );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Table created successfully!")
            return {"message": "Table created successfully!"}
        else:
            print("Failed to create table. No database connection.")
            return {"message": "Failed to create table. No database connection."}
    except psycopg2.Error as error:
        print("Error while creating table:", error)
        return {"message": "Error while creating table"}

# Add data endpoint
@app.post('/add_data')
def add_data(user_data: User):
    try:
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            # Check if user already exists
            cur.execute("SELECT * FROM users WHERE email = %s", (user_data.email,))
            existing_user = cur.fetchone()
            if existing_user:
                conn.close()
                raise HTTPException(status_code=400, detail="User already exists")

            # Hash password
            hashed_password = pwd_context.hash(user_data.password)

            # Generate public id
            public_id = str(uuid.uuid4())

            # Insert new user
            cur.execute("INSERT INTO users (public_id, name, email, password) VALUES (%s, %s, %s, %s)",
                        (public_id, user_data.name, user_data.email, hashed_password))
            conn.commit()
            conn.close()
            return {"message": "User registered successfully"}
        else:
            print("Failed to add user data. No database connection.")
            return {"message": "Failed to add user data. No database connection."}
    except psycopg2.Error as error:
        print("Error while adding user data:", error)
        return {"message": "Error while adding user data"}

# Root endpoint
@app.get('/')
def read_root():
    return {"Welcome": "Gulam Sarvar"}
