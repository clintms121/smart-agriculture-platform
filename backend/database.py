import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Use environment variables for production
DB_CONFIG = {
    """
    "dbname": os.getenv("DB_NAME", "smart_agriculture"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "YourSecurePassword123!"),
    "host": os.getenv("DB_HOST", "smart-agriculture-db.abc123.us-east-1.rds.amazonaws.com"),
    "port": int(os.getenv("DB_PORT", "5432"))
    """

    "dbname": "smart_agriculture",
    "user": "postgres",
    "password": "Owlee101#",
    "host": "localhost",
    "port": 5432

}

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

if __name__ == "__main__":
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        print("✅ RDS connected! Current time:", cur.fetchone())
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)