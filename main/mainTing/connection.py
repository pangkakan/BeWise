#Import modules
import psycopg2

#General variables
host = "pgserver.mau.se"
database = "bewise"
user = "ao9682"
password = "934ae98a"
port = "5432"  # Default PostgreSQL port

#Connect to the database
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)
cur = conn.cursor()
cur.execute("SELECT * FROM assignment")
print(cur.fetchall())
