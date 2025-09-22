import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "smart_agriculture",
    "user": "postgres",
    "password": "Owlee101#",
    "host": "localhost",
    "port": 5432
}

#function for database connection
def get_connection():
    conn = psycopg2.connect(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        cursor_factory=RealDictCursor
    )
    return conn

#test
if __name__ == "__main__":
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        print("Database connected current time: ", cur.fetchone())
        cur.close()
        conn.close()
    except Exception as e:
        print("connection failed")