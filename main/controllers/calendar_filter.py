import uuid

from models.json_manager import read_from_json_file


def filter_courses(conn, this_user):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_user_courses
     WHERE user_id = %s
    """ % this_user

    cur.execute(query)
    filtered_courses = cur.fetchall()
    formatted_courses = []
    for course in filtered_courses:
        link_id = uuid.uuid4().hex  # Generate a unique identifier for linked events
        start_event = {
            "title": course[2] + " (start)",
            "start": course[0],
            "end": course[0],
            "allDay": True,
            "linkId": link_id,

            "extendedProps": {
                "coursecode": course[2],
                "event_type": "course",
                "actualStart": course[0],
                "actualEnd": course[1],
                "description": course[3]
            }
        }
        formatted_courses.append(start_event)
        end_event = {
            "title": course[2] + " (end)",
            "start": course[1],
            "allDay": True,
            "linkId": link_id,

            "extendedProps": {
                "coursecode": course[2],
                "event_type": "course",
                "actualStart": course[0],
                "actualEnd": course[1],
                "description": course[3]
            }
        }
        formatted_courses.append(end_event)

    return formatted_courses


def filter_course_singles(conn, this_user):
    pre_formatted_courses = filter_courses(conn, this_user)
    # Adjusting events to only show start and end dates
    adjusted_events = []
    for course in pre_formatted_courses:
        link_id = uuid.uuid4().hex  # Generate a unique identifier for linked events
        start_event = {
            "title": course['title'] + " (Start)",
            "start": course['start'],
            "allDay": True,
            "linkId": link_id,
            "extendedProps": {
                "coursecode": course['coursecode'],
                "event_type": "course"
            }
        }
        adjusted_events.append(start_event)

        if course['start'] != course['end']:
            end_event = {
                "title": course['title'] + " (End)",
                "start": course['end'],  # Use the end date as the start for this event
                "allDay": True,
                "linkId": link_id,
                "extendedProps": {
                    "coursecode": course['coursecode'],
                    "event_type": "course"
                }
            }
            adjusted_events.append(end_event)
    return adjusted_events


def filter_goals(conn, this_user):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_goals
    WHERE user_id = %s
    """ % this_user
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


def filter_assignments(conn, this_user):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_assignments
    WHERE (CURRENT_DATE BETWEEN start_time AND deadline_timestamp) AND user_id = %s
    """ % this_user

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
                "completed": assignment[5],
                "goal_title": assignment[6],
                "coursecode": assignment[7],
                "event_type": "assignment"
            }
        }
        formatted_assignments.append(formatted_event)
    return formatted_assignments


def filter_course_events(conn, course_code, this_user):
    # Load events from your JSON file

    cur = conn.cursor
    query = """
    SELECT * FROM course_events
    WHERE course_code = %s AND user_id

    """

    """
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
"""

def filter_assignments_for_daily(conn, this_user):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_assignments
    WHERE (CURRENT_DATE BETWEEN start_time AND deadline_timestamp) AND user_id = %s
    """ % this_user
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


def filter_subtask(conn, this_user):
    cur = conn.cursor()
    query = """
    SELECT * FROM filter_subtasks
    WHERE CURRENT_DATE = date AND user_id = %s
    """ % this_user

    cur.execute(query)
    filtered_subtasks = cur.fetchall()
    formatted_subtasks = []
    for subtask in filtered_subtasks:
        formatted_event = {
            "id": subtask[0],
            "assignment_id": subtask[1],
            "title": subtask[2],
            "date": subtask[3],
            "completed": subtask[4]
        }
        formatted_subtasks.append(formatted_event)
    return formatted_subtasks
