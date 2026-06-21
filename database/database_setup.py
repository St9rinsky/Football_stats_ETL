from connection import db_connect

def setup_schema():
    connection = db_connect()
    cursor = connection.cursor()

    try:
        with open("database/create_schema.sql") as f:
            cursor.execute(f.read())

        connection.commit()

    finally:
        cursor.close()
        connection.close()

def setup_silver_tables():
    connection = db_connect()
    cursor = connection.cursor()

    try:
        with open("database/silver_tables.sql") as f:
            cursor.execute(f.read())

        connection.commit()

    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    setup_silver_tables()
