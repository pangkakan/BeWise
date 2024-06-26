import json
import logging
from datetime import datetime
import traceback

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
from models.scraper import Scraper

TEMPLATE_PATH.append('main/views')

conn = create_connection()
current_user = 2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@route("/")
def index():
    # course_events_today
    # user_events_today
    nested_assignments = fetch_todo_subtasks()
    #print(nested_assignments)
    card_data = fetch_card_data()
    return template("index", user=current_user, todo_tasks=nested_assignments, card_data=card_data)


@route("/switch-user/<id>")
def switch_user(id):
    global current_user
    if id != current_user:
        current_user = id
        print(f"Switching to user: {id}")
        response.status = 204
        response.set_header('HX-Redirect', '/')
        return ''


@route("/todo-update/<id>", method="patch")
def todo_update(id):

    #conn.autocommit = False  # Start transaction

    cur = conn.cursor()

    try:
        # Step 1: Toggle the subtask's completed status
        toggle_subtask_query = """
        UPDATE subtasks
        SET completed = NOT completed
        WHERE id = %s
        RETURNING completed;
        """
        cur.execute(toggle_subtask_query, (id,))
        subtask_completed = cur.fetchone()[0]

        print("Subtask toggled successfully. New completed status:", subtask_completed)

        # Step 2: Update the assignment's completed status
        update_assignment_query = """
        WITH updated_assignment AS (
            SELECT assignment_id
            FROM subtasks
            WHERE id = %s
        )
        UPDATE assignments
        SET completed = (
            SELECT NOT EXISTS (
                SELECT 1
                FROM subtasks
                WHERE assignment_id = updated_assignment.assignment_id
                AND completed = FALSE
            )
        )
        FROM updated_assignment
        WHERE assignments.id = updated_assignment.assignment_id
        RETURNING assignments.goal_id;
        """
        cur.execute(update_assignment_query, (id,))
        goal_id = cur.fetchone()[0]

        print("Assignment updated successfully.")

        # Step 3: Update the goal's completed status
        update_goal_query = """
        UPDATE goals
        SET completed = (
            SELECT NOT EXISTS (
                SELECT 1
                FROM assignments
                WHERE goal_id = %s
                AND completed = FALSE
            )
        )
        WHERE id = %s;
        """
        cur.execute(update_goal_query, (goal_id, goal_id))

        print("Goal updated successfully.")

        # Commit the transaction
        conn.commit()

        print("Subtask and related assignment and goal updated successfully.")
        response.status = 204
        response.set_header('HX-Redirect', '/')
        return ''

    except Exception as e:
        print("Error occurred during database operation:", e)
        print("Database error message:", cur.statusmessage)
        conn.rollback()  # Rollback the transaction in case of error
        response.status = 204
        response.set_header('HX-Redirect', '/')
        return ''





def fetch_todo_subtasks():
    cur = conn.cursor()
    query = """
    SELECT 
    a.id AS assignment_id,
    a.title AS assignment_title,
    ARRAY_AGG(
        JSON_BUILD_OBJECT(
            'title', s.title, 
            'id', s.id, 
            'date', s.date, 
            'completed', s.completed
        )
    ) AS subtasks
    FROM users u 
        JOIN user_courses uc ON u.id = uc.user_id
        JOIN courses c ON uc.course_id = c.id
        JOIN goals g ON uc.id = g.user_course_id
        JOIN assignments a ON g.id = a.goal_id
        JOIN subtasks s ON a.id = s.assignment_id
    WHERE u.id = %s 
    AND CURRENT_DATE = s.date 
    GROUP BY a.id, a.title;

    """ % current_user
    cur.execute(query)
    this_user_todo_today = cur.fetchall()
    assignments = []
    for row in this_user_todo_today:
        assignment = {
            "id": row[0],
            "title": row[1],
            "subtasks": row[2]
        }
        assignments.append(assignment)
    return assignments


def fetch_card_data():
    cur = conn.cursor()
    query = """
    SELECT 
        g.id AS goal_id,
        g.title AS goal_title,
        g.deadline_timestamp AS goal_deadline,
        c.title AS course_title,
        JSON_AGG(
            JSON_BUILD_OBJECT(
                'assignment_id', a.id,
                'assignment_title', a.title,
                'deadline_timestamp', a.deadline_timestamp,
                'completed', a.completed,
                'subtasks', (
                    SELECT JSON_AGG(
                                JSON_BUILD_OBJECT(
                                    'title', s.title, 
                                    'id', s.id, 
                                    'completed', s.completed
                                )
                            )
                    FROM subtasks s
                    WHERE s.assignment_id = a.id
                )
            )
        ) AS assignments
    FROM users u 
    JOIN user_courses uc ON u.id = uc.user_id
    JOIN courses c ON uc.course_id = c.id
    JOIN goals g ON uc.id = g.user_course_id
    JOIN assignments a ON g.id = a.goal_id
    WHERE u.id = %s
    GROUP BY g.id, g.title, g.deadline_timestamp, c.title;
    """ % current_user

    cur.execute(query)
    this_user_card_data = cur.fetchall()
    goals = []

    for row in this_user_card_data:
        goal = {
            "id": row[0],
            "title": row[1],
            "deadline_timestamp": row[2],
            "course_title": row[3],
            "assignments": row[4] if row[4] else []
        }
        goals.append(goal)

    return goals



def calculate_completion_stats(goals):
    for goal in goals:
        total_assignments = len(goal["assignments"])
        completed_assignments = 0
        total_subtasks = 0
        completed_subtasks = 0

        for assignment in goal["assignments"]:
            if assignment["completed"]:
                completed_assignments += 1

            if assignment["subtasks"]:  # Check if subtasks list is not None
                for subtask in assignment["subtasks"]:
                    total_subtasks += 1
                    if subtask["completed"]:
                        completed_subtasks += 1

        goal["assignments_summary"] = {
            "completed": completed_assignments,
            "total": total_assignments
        }
        goal["subtasks_summary"] = {
            "completed": completed_subtasks,
            "total": total_subtasks
        }

    return goals



@route("/add-course", method="post")
def add_course():
    given_course_code = request.forms.get("course_code").lower()
    start_date = "2024-01-01 00:00:00"
    end_date = "2024-06-02 00:00:00"

    try:
        with conn.cursor() as cur:
            # Check if course exists
            cur.execute("SELECT id FROM courses WHERE course_code = %s", (given_course_code,))
            course_id = cur.fetchone()

            if course_id:
                course_id = course_id[0]
                # Check if user is already connected to the course
                cur.execute("SELECT id FROM user_courses WHERE user_id = %s AND course_id = %s", (current_user, course_id))
                user_course_id = cur.fetchone()

                if not user_course_id:
                    # Connect user to a course in db
                    cur.execute("INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s)", (current_user, course_id))
                    conn.commit()
                    return "success"
                else:
                    print("User already connected to course")
                    return "User already connected to course"
            else:
                # If course does not exist, create it and connect the user
                course_title = Scraper(given_course_code, True).extract_course_name()
                cur.execute(
                    "INSERT INTO courses (start_timestamp, end_timestamp, course_code, title) VALUES (%s, %s, %s, %s) RETURNING id",
                    (start_date, end_date, given_course_code, course_title)
                )
                created_course_id = cur.fetchone()[0]
                conn.commit()

                cur.execute("INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s)", (current_user, created_course_id))
                conn.commit()

                scrape_to_db(conn, given_course_code, True)
                return "success"



    except Exception as e:
        traceback.print_exc()

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

        cur.close()
        return "success"

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Insert failed: {e}")
        cur.close()



@route("/add-assignment", method="post")
def add_assignment():
    goal_id = request.forms.get("chosen_goal")
    # startdate and enddate boundary = goal startdate-enddate
    start_date = request.forms.get("assignment_startdate")
    end_date = request.forms.get("assignment_enddate")
    title = request.forms.get("assignment_title")
    type = request.forms.get("assignment_type")
    prio = request.forms.get("chosen_prio")
    print(f"Goal id: {goal_id}, Start: {start_date}, End: {end_date}, Title: {title}, Type: {type}")

    # insert into db
    cur = conn.cursor()

    insert_query = """
        INSERT INTO assignments (goal_id, title, start_time, deadline_timestamp, type, priority)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    values = (goal_id, title, start_date, end_date, type, prio)

    try:
        # Execute query and check if insert is successful
        cur.execute(insert_query, values)

        inserted_id = cur.fetchone()[0]

        conn.commit()

        print(f"Insert successful, new row id: {inserted_id}")

        cur.close()
        return "success"

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Insert failed: {e}")
        cur.close()



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

        cur.close()
        return "success"

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Insert failed: {e}")
        cur.close()


@route("/add-event", method="post")
def add_event():
    #weekday = request.forms.get("chosen_weekday")
    return "success"


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
    cur = conn.cursor()
    query = """
    SELECT g.title, g.id FROM users u 
    JOIN user_courses uc ON u.id = uc.user_id
    JOIN courses c ON uc.course_id = c.id
    JOIN public.goals g on uc.id = g.user_course_id
    WHERE user_id = %s
     
    """ % current_user
    cur.execute(query)
    this_user_goals = cur.fetchall()
    goal_list = []
    for goal in this_user_goals:
        goal = {
            "title": goal[0],
            "id": goal[1]
        }
        goal_list.append(goal)

    # get all user goals (goal id + title) from database
    return template("goal-select", goals=goal_list)


@route("/get-user-assignments")
def get_user_goals():
    assignments = ["Första uppgiften", "Andra uppgiften", "Tredje uppgiften"]
    # get all user assignments (assignment id + title) from database
    cur = conn.cursor()
    query = """
    SELECT a.title, a.id FROM users u 
    JOIN user_courses uc ON u.id = uc.user_id
    JOIN courses c ON uc.course_id = c.id
    JOIN goals g on uc.id = g.user_course_id
    JOIN assignments a on g.id = a.goal_id
    WHERE user_id = %s
     
    """ % current_user
    cur.execute(query)
    this_user_assignments = cur.fetchall()
    assignment_list = []
    for assignment in this_user_assignments:
        assignment = {
            "title": assignment[0],
            "id": assignment[1]
        }
        assignment_list.append(assignment)

    return template("assignment-select", assignments=assignment_list)



@route("/view-courses")
def view_courses():
    courses = ["DA336A - Systemutveckling startdaum slutdatum", "DA297A - Databasteknik startdatum slutdatum", "DA354A - Programmering startdatum slutdatum"]
    # get all user courses (id, coursecode, title, start, end) from database

    cur = conn.cursor()

    query = """
    SELECT c.title, uc.id, c.start_timestamp, c.end_timestamp, c.course_code FROM users u 
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
            "id": course[1],
            "start": course[2],
            "end": course[3],
            "code": course[4]
        }
        course_list.append(course)

    return template("view-courses-list", user_courses=course_list)


@route("/view-goals")
def view_goals():
    goals = ["Mål 1", "Mål 2", "Mål 3"]
    # get all user goals (id, course, title, start, end, type, completed) from database
    cur = conn.cursor()
    query = """
    SELECT g.id, g.title, g.start_time, g.deadline_timestamp, g.type, g.completed FROM users u 
    JOIN user_courses uc ON u.id = uc.user_id
    JOIN courses c ON uc.course_id = c.id
    JOIN public.goals g on uc.id = g.user_course_id
    WHERE user_id = %s
     
    """ % current_user
    cur.execute(query)
    this_user_goals = cur.fetchall()
    goal_list = []
    for goal in this_user_goals:
        goal = {
            "id": goal[0],
            "title": goal[1],
            "start": goal[2],
            "end": goal[3],
            "type": goal[4],
            "completed": goal[5]
        }
        goal_list.append(goal)

    return template("view-goals-list", goals=goal_list)


@route("/view-assignments")
def view_assignments():
    assignments = ["Uppgift 1", "Uppgift 2", "Uppgift 3"]
    # get all user assignments (id, goal, title, start, end, type, priority, completed) from database
    cur = conn.cursor()
    query = """
    SELECT a.id, a.title, a.start_time, a.deadline_timestamp, a.type, a.priority, a.completed FROM users u 
    JOIN user_courses uc ON u.id = uc.user_id
    JOIN courses c ON uc.course_id = c.id
    JOIN goals g on uc.id = g.user_course_id
    JOIN assignments a on g.id = a.goal_id
    WHERE user_id = %s
     
    """ % current_user
    cur.execute(query)
    this_user_assignments = cur.fetchall()
    assignment_list = []
    for assignment in this_user_assignments:
        assignment = {
            "id": assignment[0],
            "title": assignment[1],
            "start": assignment[2],
            "end": assignment[3],
            "type": assignment[4],
            "priority": assignment[5],
            "completed": assignment[6]
        }
        assignment_list.append(assignment)

    return template("view-assignments-list", assignments=assignment_list)


@route("/view-subtasks")
def view_subtasks():
    subtasks = ["Deluppgift 1", "Deluppgift 2", "Deluppgift 3"]
    # get all user subtasks (id, assignment, title, date, type, completed) from database

    cur = conn.cursor()
    query = """
    SELECT s.title, s.id, s.date, s.completed FROM users u 
    JOIN user_courses uc ON u.id = uc.user_id
    JOIN courses c ON uc.course_id = c.id
    JOIN goals g on uc.id = g.user_course_id
    JOIN assignments a on g.id = a.goal_id
    JOIN subtasks s on a.id = s.assignment_id
    WHERE user_id = %s
     
    """ % current_user
    cur.execute(query)
    this_user_subtasks = cur.fetchall()
    subtask_list = []
    for subtask in this_user_subtasks:
        subtask = {
            "title": subtask[0],
            "id": subtask[1],
            "date": subtask[2],
            "completed": subtask[3]
        }
        subtask_list.append(subtask)
    return template("view-subtasks-list", subtasks=subtask_list)


@route("/view-events")
def view_events():
    events = ["Händelse 1", "Händelse 2", "Händelse 3"]
    # get all user events from database
    return template("view-events-list", events=events)



@route("/delete-course/<id>", method="delete")
def delete_course(id):
    cur = conn.cursor()
    query = """
     DELETE FROM user_courses WHERE id = %s
    """ % id

    try:
        cur.execute(query)
        conn.commit()
        return "success"
    except Exception as e:
        conn.rollback()
        print(f"Delete failed: {e}")
        cur.close()



@route("/delete-goal/<id>", method="delete")
def delete_goal(id):
    cur = conn.cursor()

    delete_query = """
        DELETE FROM goals WHERE id = %s
     
    """ % id

    try:
        # Execute query and check if delete is successful
        cur.execute(delete_query)
        conn.commit()

        if cur.rowcount > 0:
            print("Deletion successful.")
            cur.close()
            return "success"
        else:
            print("No rows deleted. Item with ID", id, "not found.")
            cur.close()

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Delete failed: {e}")
        cur.close()



@route("/delete-assignment/<id>", method="delete")
def delete_assignment(id):
    cur = conn.cursor()

    delete_query = """
        DELETE FROM assignments WHERE id = %s
     
    """ % id

    try:
        # Execute query and check if delete is successful
        cur.execute(delete_query)
        conn.commit()

        if cur.rowcount > 0:
            print("Deletion successful.")
            cur.close()
            return "success"
        else:
            print("No rows deleted. Item with ID", id, "not found.")
            cur.close()

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Delete failed: {e}")
        cur.close()


@route("/delete-subtask/<id>", method="delete")
def delete_subtask(id):
    cur = conn.cursor()

    delete_query = """
        DELETE FROM subtasks WHERE id = %s
     
    """ % id

    try:
        # Execute query and check if delete is successful
        cur.execute(delete_query)
        conn.commit()

        if cur.rowcount > 0:
            print("Deletion successful.")
            cur.close()
            return "success"
        else:
            print("No rows deleted. Item with ID", id, "not found.")
            cur.close()

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Delete failed: {e}")
        cur.close()



@route("/delete-event/<id>", method="delete")
def delete_event(id):
    return "success"



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
