import json
import logging
from bottle import route, run, template, error, static_file, request, redirect, response, TEMPLATE_PATH
from controllers import course_controller as course_ctrl
from datetime import datetime
from controllers.db import create_connection
from controllers.task_controller import (
    add_task_post,
    get_tasks_with_coursecode,
    get_task_with_id,
)
from controllers.timeblock_controller import (
    add_timeblock_post,
    get_timeblocks_with_coursecode,
    get_timeblock_with_id,
)
from controllers.calendar_filter import (
    filter_courses,
    filter_goals,
    filter_assignments,
    filter_course_events, filter_assignments_for_daily, filter_course_singles, filter_subtask
)
from models.events import scrape_to_db
from models.json_manager import read_from_json_file, DateTimeEncoder

TEMPLATE_PATH.append('main/views')

conn = create_connection()
current_user = 2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@route("/")
def index():
    today_tasks = get_today_tasks()
    goals = filter_goals(conn, current_user)
    return template("index", today_tasks=today_tasks, goals=goals)


def nested_user_data():
    pass


def get_today_tasks():
    # all_tasks = []
    # all_tasks += filter_assignments_for_daily(conn)
    all_subtasks = []
    all_subtasks += filter_subtask(conn, current_user)
    return all_subtasks


@route("/<coursecode>")
def course_page(coursecode):
    # kontrollera att kurs med den coursecodeen finns i courses.json
    try:
        course = course_ctrl.get_course_with_coursecode(coursecode)
        return template("coursepage", course=course)
    except:
        return template("error")


@route("/new-course")
def new_course():
    return template("addcourse")


@route("/add-course", method="post")
def add_course():
    course_code = request.forms.get("course_code")

    # check if coursecode exists for some course
    # check if user is already connected to the course

    # connect user to a course in db



@route("/add-goal", method="post")
def add_goal():
    user_course_id = request.forms.get("chosen_course")

    start_date = request.forms.get("goal_startdate")
    end_date = request.forms.get("goal_enddate")
    title = request.forms.get("goal_title")
    goal_type = request.forms.get("goal_type")
    logger.debug(f"Course id: {user_course_id}, Start: {start_date}, End: {end_date}, Title: {title}, Type: {goal_type}")

    cur = conn.cursor()

    insert_query = """
        INSERT INTO goals (user_course_id, title, start_time, deadline_timestamp, type)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """

    values = (user_course_id, title, start_date, end_date, goal_type)

    try:
        # Execute query and check if insert is successful
        cur.execute(insert_query, values)

        inserted_id = cur.fetchone()[0]

        conn.commit()

        print(f"Insert successful, new row id: {inserted_id}")

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Insert failed: {e}")




@route("/add-assignment", method="post")
def add_assignment():
    goal_id = request.forms.get("chosen_goal")
    # startdate and enddate boundary = goal startdate-enddate
    start_date = request.forms.get("assignment_startdate")
    end_date = request.forms.get("assignment_enddate")
    title = request.forms.get("assignment_title")
    type = request.forms.get("assignment_type")
    print(f"Goal id: {goal_id}, Start: {start_date}, End: {end_date}, Title: {title}, Type: {type}")

    # insert into db
    cur = conn.cursor()

    insert_query = """
        INSERT INTO assignments (goal_id, title, start_time, deadline_timestamp, type)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """

    values = (goal_id, title, start_date, end_date, type)

    try:
        # Execute query and check if insert is successful
        cur.execute(insert_query, values)

        inserted_id = cur.fetchone()[0]

        conn.commit()

        print(f"Insert successful, new row id: {inserted_id}")

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Insert failed: {e}")


@route("/add-subtask", method="post")
def add_subtask():
    assignment_id = request.forms.get("chosen_assignment")
    # date boundary = assignment startdate-enddate
    date = request.forms.get("subtask_date")
    title = request.forms.get("subtask_title")
    print(f"Assignment id: {assignment_id}, Date: {date}, Title: {title}")

    # insert into db
    cur = conn.cursor()

    insert_query = """
        INSERT INTO subtasks (assignment_id, title, date)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    values = (assignment_id, title, date)

    try:
        # Execute query and check if insert is successful
        cur.execute(insert_query, values)

        inserted_id = cur.fetchone()[0]

        conn.commit()

        print(f"Insert successful, new row id: {inserted_id}")

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Insert failed: {e}")


@route("/add-event", method="post")
def add_event():
    weekday = request.forms.get("chosen_weekday")


@route("/get-user-courses")
def get_user_courses():

    cur = conn.cursor()

    query = """
    SELECT c.title, uc.id FROM users u 
    JOIN user_courses uc ON u.id = uc.user_id
    JOIN courses c ON uc.course_id = c.id
    WHERE user_id = %s
     
    """ % current_user
    cur.execute(query)
    this_user_courses = cur.fetchall()
    course_list = []
    for course in this_user_courses:
        course = {
            "title": course[0],
            "id": course[1]
        }
        course_list.append(course)


    # get all user courses (course id + title)
    return template("course-select", courses=course_list)


@route("/get-user-courses/events")
def get_user_courses():
    courses = ["Systemutveckling", "Databasteknik", "Programmering"]
    # get all user courses (course id + title)
    return template("event-course-select", courses=courses)


@route("/get-user-goals")
def get_user_goals():
    goals = ["Första målet", "Andra målet", "Tredje målet"]
    # get all user goals (goal id + title) from database
    return template("goal-select", goals=goals)


@route("/get-user-assignments")
def get_user_goals():
    assignments = ["Första uppgiften", "Andra uppgiften", "Tredje uppgiften"]
    # get all user assignments (assignment id + title) from database
    return template("assignment-select", assignments=assignments)



@route("/view-courses")
def view_courses():
    courses = ["DA336A - Systemutveckling startdaum slutdatum", "DA297A - Databasteknik startdatum slutdatum", "DA354A - Programmering startdatum slutdatum"]
    # get all user courses (id, coursecode, title, start, end) from database
    return template("view-courses-list", courses=courses)


@route("/view-goals")
def view_goals():
    goals = ["Mål 1", "Mål 2", "Mål 3"]
    # get all user goals (id, course, title, start, end, type, completed) from database
    return template("view-goals-list", goals=goals)


@route("/view-assignments")
def view_assignments():
    assignments = ["Uppgift 1", "Uppgift 2", "Uppgift 3"]
    # get all user assignments (id, goal, title, start, end, type, priority, completed) from database
    return template("view-assignments-list", assignments=assignments)


@route("/view-subtasks")
def view_subtasks():
    subtasks = ["Deluppgift 1", "Deluppgift 2", "Deluppgift 3"]
    # get all user subtasks (id, assignment, title, date, type, completed) from database
    return template("view-subtasks-list", subtasks=subtasks)


@route("/view-events")
def view_events():
    events = ["Händelse 1", "Händelse 2", "Händelse 3"]
    # get all user events from database
    return template("view-events-list", events=events)



@route("/api/calendar")
def calendar_api():
    types = request.query.get('types', '')
    type_list = types.split(',') if types else []

    all_events = []

    all_events += filter_courses(conn, current_user)
    if "goals" in type_list:
        all_events += filter_goals(conn, current_user)
    if "assignments" in type_list:
        all_events += filter_assignments(conn, current_user)
    if "course_events" in type_list:
        all_events += filter_course_events(conn, current_user)

    # Return the formatted events
    response.content_type = 'application/json'
    return json.dumps(all_events, cls=DateTimeEncoder)


@route("/api/today-tasks")
def today_tasks():


    all_tasks = []
    all_tasks += filter_subtask(conn, 2)

    response.content_type = 'application/json'
    return json.dumps(all_tasks, cls=DateTimeEncoder)



@error(404)
def error404(error):
    """
    Visar felmeddelande för sida som ej existerar

    Returnerar error.html
    """
    return template("error")


@route("/static/<filename>")
def static_files(filename):
    """
    Handles the routes to our static files

        Returns:
                file : the static file requested by URL
    """
    return static_file(filename, root="static")


# Start our web server
run(host="127.0.0.1", port=8080, reloader=True)
