from models.scraper import Scraper


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

def scrape_to_db(conn, course_code, course_or_no):
    cur = conn.cursor()
    events = Scraper(course_code, course_or_no).scrape()
    for week_events in events.values():
        for event in week_events:
            cur.execute(
                "INSERT INTO course_events (day, date, start_time, end_time, location, description, course_code) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    event["day"],
                    event["date"],
                    event["start_time"],
                    event["end_time"],
                    event["location"],
                    event["description"],
                    course_code,
                ),
            )
    conn.commit()
