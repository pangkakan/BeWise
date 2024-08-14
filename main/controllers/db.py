import psycopg2


def create_connection():
    # General variables
    host = "pgserver.mau.se"
    database = "bewise"
    user = "ao9682"
    password = "934ae98a"
    port = "5432"  # Default PostgreSQL port
    return psycopg2.connect(
        host=host, database=database, user=user, password=password, port=port
    )

'''
def create_table():
    # Creating the table for users in python becuase i could not login into pgadmin...
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS user_data (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL
    );
    """
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute(create_table_sql)
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("Table created successfully.")
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while creating table: {error}")

create_table()'''
def print_all_users():
    """
    Fetches and prints all the users from the user_data table.
    """
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_data")
        rows = cur.fetchall()
        
        print("Contents of user_data table:")
        for row in rows:
            print(row)
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching users: {e}")
print_all_users()