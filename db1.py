import psycopg2

def get_connection1():
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



def create_table1():
    try:
        db_conn=psycopg2.connect(database="BlueBash", user="postgres", 
                                 password="7895", host="127.0.0.1", port="5432")()
        if db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS userdata (
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

