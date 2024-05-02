import psycopg2

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


def create_table():
    try:
        db_conn = get_connection()
        if db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS login (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
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


def add_data(query, data):
    try:
        db_conn = get_connection()
        if db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(query, data)
            db_conn.commit()
            db_cursor.close()
            db_conn.close()
            print("Data inserted successfully!")
            return True
        else:
            print("Failed to insert data. No database connection.")
            return False
    except Exception as e:
        print("Error while inserting data:", e)
        return False


def update_data(query, data):
    print(data)
    try:
        db_conn = get_connection()
        if db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(query, data)
            db_conn.commit()
            db_cursor.close()
            db_conn.close()
            print("Data updated successfully!")
            return True
        else:
            print("Failed to update data. No database connection.")
            return False
    except Exception as e:
        print("Error while updating data:", e)
        return False


def print_data(query, data):
    try:
        db_conn=get_connection()
        if db_conn:
            db_cursor=db_conn.cursor()
            db_cursor.execute(query, data)
            result=db_cursor.fetchall()
            db_cursor.close()
            db_conn.close()
            return result
        else:
            print("Failed to print data. No database connection.")
            return False
    except Exception as e:
        print("Error while printing data:", e)
        return False


async def login_data(username, password):
    try:
        db_conn=psycopg2.connect(database="BlueBash", user="postgres", 
                                 password="7895", host="127.0.0.1", port="5432")
        db_cursor = db_conn.cursor()
        query="""select * from login where username = %s and password = %s """
        db_cursor.execute(query, (username, password))
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        if db_cursor.rowcount == 1:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password!")
            return False
    except:
        print("login failed")
        return False


def delete_data1(query, data):
    try:
        db_conn=psycopg2.connect(database="BlueBash", user="postgres", 
                                 password="7895", host="127.0.0.1", port="5432")
        db_cursor=db_conn.cursor()
        db_cursor.execute(query, data)
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
        deleted_rows = db_cursor.rowcount
        print(deleted_rows)
        if deleted_rows > 0:
            print("Data deleted successfully!")
            return True
        else:
            print("No data found to delete with the provided parameters.")
            return False
    except Exception as e:
        print("Error while deleting data:", e)
        return False
    
