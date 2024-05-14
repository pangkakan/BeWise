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
                "coursecode": course[2]
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
        start_datetime = f"{goal['date']}T{goal['start_time']}"
        end_datetime = f"{goal['date']}T{goal['deadline']}"
        formatted_event = {
            "title": goal["title"],
            "start": start_datetime,
            "end": end_datetime,
            "extendedProps": {
                "type": goal["type"],
                "coursecode": goal["coursecode"]
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
        start_datetime = f"{assignment['date']}T{assignment['start_time']}"
        end_datetime = f"{assignment['date']}T{assignment['deadline']}"
        formatted_event = {
            "title": assignment["title"],
            "start": start_datetime,
            "end": end_datetime,
            "extendedProps": {
                "type": assignment["type"],
                "priority": assignment["priority"],
                "goal_title": assignment["goal_title"],
                "coursecode": assignment["coursecode"]
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
                "coursecode": event["coursecode"]
            }
        }
        formatted_events.append(formatted_event)
    return formatted_events


