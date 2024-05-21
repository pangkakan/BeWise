from models.json_manager import read_from_json_file


def filter_courses(conn):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_courses
    """
    cur.execute(query)
    filtered_courses = cur.fetchall()
    formatted_courses = []
    for course in filtered_courses:
        formatted_event = {
            "title": course[3],
            "start": course[0],
            "end": course[1],
            "extendedProps": {
                "coursecode": course[2],
                "event_type": "course"
            }
        }
        formatted_courses.append(formatted_event)
    return formatted_courses


def filter_goals(conn):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_goals
    """
    cur.execute(query)
    filtered_goals = cur.fetchall()
    formatted_goals = []
    for goal in filtered_goals:
        formatted_event = {
            "title": goal[0],
            "start": goal[1],
            "end": goal[2],
            "extendedProps": {
                "type": goal[3],
                "coursecode": goal[4],
                "event_type": "goal"
            }
        }
        formatted_goals.append(formatted_event)
    return formatted_goals


def filter_assignments(conn):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_assignments
    """
    cur.execute(query)
    filtered_assignments = cur.fetchall()
    formatted_assignments = []
    for assignment in filtered_assignments:
        formatted_event = {
            "title": assignment[0],
            "start": assignment[1],
            "end": assignment[2],
            "extendedProps": {
                "type": assignment[3],
                "priority": assignment[4],
                "goal_title": assignment[5],
                "coursecode": assignment[6],
                "event_type": "assignment"
            }
        }
        formatted_assignments.append(formatted_event)
    return formatted_assignments


def filter_course_events():
    # Load events from your JSON file
    events = read_from_json_file("static/timeblocks.json")

    # Convert the events to FullCalendar's format
    formatted_events = []
    for event in events:
        start_datetime = f"{event['date']}T{event['start_time']}"
        end_datetime = f"{event['date']}T{event['end_time']}"
        formatted_event = {
            "title": event["description"],
            "start": start_datetime,
            "end": end_datetime,
            "extendedProps": {
                "location": event["location"],
                "coursecode": event["coursecode"],
                "event_type": "course_event"
            }
        }
        formatted_events.append(formatted_event)
    return formatted_events


def filter_assignments_for_daily(conn):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_assignments

    """
    cur.execute(query)
    filtered_assignments = cur.fetchall()
    formatted_assignments = []
    for assignment in filtered_assignments:
        formatted_event = {
            "title": assignment[0],
            "start": assignment[1],
            "end": assignment[2],
            "extendedProps": {
                "type": assignment[3],
                "priority": assignment[4],
                "goal_title": assignment[5],
                "coursecode": assignment[6],
                "event_type": "assignment"
            }
        }
        formatted_assignments.append(formatted_event)
    print(formatted_assignments)
    return formatted_assignments