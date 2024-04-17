import json
import psycopg2


def get_events(conn):
    cur = conn.cursor()
    # Fetch events and convert date and time columns to string format
    query = """
    SELECT id, date::text, start_time::text, end_time::text, location, description FROM events
    """
    cur.execute(query)
    events = cur.fetchall()

    # Convert query results into a list of dicts to serialize to JSON
    columns = [desc[0] for desc in cur.description]
    return [dict(zip(columns, row)) for row in events]
