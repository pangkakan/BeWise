import json

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
    filter_course_events, filter_assignments_for_daily,
    filter_subtasks
)
from models.json_manager import read_from_json_file, DateTimeEncoder

TEMPLATE_PATH.append('main/views')

conn = create_connection()


@route("/")
def index():
    today_tasks = get_today_tasks()
    goals = filter_goals(conn)
    return template("index", today_tasks=today_tasks, goals=goals)


def nested_user_data():
    pass


def get_today_tasks():
    # all_tasks = []
    # all_tasks += filter_assignments_for_daily(conn)
    all_subtasks = []
    all_subtasks += filter_subtasks(conn)
    return all_subtasks


# @route("/<coursecode>")
# def course_page(coursecode):
#     # kontrollera att kurs med den coursecodeen finns i courses.json
#     try:
#         course = course_ctrl.get_course_with_coursecode(coursecode)
#         return template("coursepage", course=course)
#     except:
#         return template("error")


# @route("/new-course")
# def new_course():
#     return template("addcourse")


# @route("/add-course", method="post")
# def handle_add_course():
#     return course_ctrl.add_course_post(conn)

@route("/add-course", method="post")
def add_course():
    course_code = request.forms.get("course_code")
    
    # check if coursecode exists for some course
    # check if user is already connected to the course 

    # connect user to a course in db
    


@route("/add-goal", method="post")
def add_goal():
    user_course_id = request.forms.get("chosen_course")
    # startdate and enddate boundary = course startdate-enddate
    start_date = request.forms.get("goal_startdate")
    end_date = request.forms.get("goal_enddate")
    title = request.forms.get("goal_title")
    type = request.forms.get("goal_type")
    print(f"Course id: {user_course_id}, Start: {start_date}, End: {end_date}, Title: {title}, Type: {type}")

    # insert into db


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


@route("/add-subtask", method="post")
def add_subtask():
    assignment_id = request.forms.get("chosen_assignment") 
    # date boundary = assignment startdate-enddate
    date = request.forms.get("subtask_date")
    title = request.forms.get("subtask_title")
    print(f"Assignment id: {assignment_id}, Date: {date}, Title: {title}")

    # insert into db


@route("/add-event", method="post")
def add_event():
    weekday = request.forms.get("chosen_weekday")


@route("/get-user-courses")
def get_user_courses():
    courses = ["Systemutveckling", "Databasteknik", "Programmering"]
    # get all user courses (course id + title)
    return template("course-select", courses=courses)


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


# @route("/<coursecode>/tasks")
# def course_tasks(coursecode):
#     # läs in alla uppgifter för coursecode och skicka till tasks.html
#     try:
#         course = course_ctrl.get_course_with_coursecode(coursecode)
#         tasks = get_tasks_with_coursecode(coursecode)
#         return template("tasks", course=course, tasks=tasks)

#     except:
#         return template("error")


# @route("/<coursecode>/tasks/<id>")
# def view_task(coursecode, id):
#     # hämta uppgift med rätt id från uppgiftslistan och skicka till task.html
#     try:
#         course = course_ctrl.get_course_with_coursecode(coursecode)
#         task = get_task_with_id(coursecode, id)
#         return template("task", course=course, task=task)

#     except:
#         return template("error")


# @route("/add-task", method="post")
# def handle_add_task():
#     return add_task_post()


# @route("/<coursecode>/schedule")
# def course_tasks(coursecode):
#     # läs in alla tidsblock för coursecode och skicka till schedule.html
#     try:
#         course = course_ctrl.get_course_with_coursecode(coursecode)
#         timeblocks = get_timeblocks_with_coursecode(coursecode)
#         return template("schedule", course=course, timeblocks=timeblocks)

#     except:
#         return template("error")


# @route("/<coursecode>/schedule/<id>")
# def view_timeblock(coursecode, id):
#     # hämta tidsblock med rätt id från tidsblocklistan och skicka till timeblock.html
#     try:
#         course = course_ctrl.get_course_with_coursecode(coursecode)
#         timeblock = get_timeblock_with_id(coursecode, id)
#         return template("timeblock", course=course, timeblock=timeblock)

#     except:
#         return template("error")


# @route("/add-timeblock", method="post")
# def handle_add_timeblock():
#     return add_timeblock_post()


# @route("/preferences")
# def study_preferences():
#     return template("studypreferences")


# @route("/save-preferences", method="post")
# def add_preferences():
#     hours_per_week = getattr(request.forms, "rangeInput")
#     # skriv till fil

#     # flash message("Dina preferenser har sparats")
#     redirect("/profile")


# @route("/profile")
# def show_profile():
#     return template("profile")


@route("/api/calendar")
def calendar_api():
    types = request.query.get('types', '')
    type_list = types.split(',') if types else []

    all_events = []

    all_events += filter_courses(conn)
    if "goals" in type_list:
        all_events += filter_goals(conn)
    if "assignments" in type_list:
        all_events += filter_assignments(conn)
    if "course_events" in type_list:
        all_events += filter_course_events()




    # Return the formatted events
    response.content_type = 'application/json'
    return json.dumps(all_events, cls=DateTimeEncoder)


@route("/api/today-tasks")
def today_tasks():


    all_tasks = []
    all_tasks += filter_assignments_for_daily(conn)

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
