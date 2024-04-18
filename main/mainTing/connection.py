# Import modules
import psycopg2

from mainTing.scraper import Scraper

# General variables
host = "pgserver.mau.se"
database = "bewise"
user = "ao9682"
password = "934ae98a"
port = "5432"  # Default PostgreSQL port

# Connect to the database
conn = psycopg2.connect(
    host=host, database=database, user=user, password=password, port=port
)
cur = conn.cursor()
eventsen = Scraper("da336a", True).scrape()
for week_events in eventsen.values():
    for event in week_events:
        cur.execute(
            "INSERT INTO events (day, date, start_time, end_time, location, description, course_code) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                event["day"],
                event["date"],
                event["start_time"],
                event["end_time"],
                event["location"],
                event["description"],
                "da336a",
            ),
        )
conn.commit()
