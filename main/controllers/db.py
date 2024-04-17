import psycopg2

def create_connection():
    #General variables
    host = "pgserver.mau.se"
    database = "bewise"
    user = "ao9682"
    password = "934ae98a"
    port = "5432"  # Default PostgreSQL port
    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )