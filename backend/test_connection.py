import psycopg2

def connect_database():
    conn = None
    try:
        conn = psycopg2.connect("dbname=smart_agriculture user=postgre password=Owlee101#")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return False
