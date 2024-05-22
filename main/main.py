import json

from bottle import route, run, template, error, static_file, request, redirect, response
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
from models.json_manager import read_from_json_file, DateTimeEncoder

conn = create_connection()
current_user = 1

@route("/")
def index():
    # Lista av kurser
    # fem

    return template("schedule")

"""
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
def handle_add_course():
    return course_ctrl.add_course_post(conn)


@route("/<coursecode>/tasks")
def course_tasks(coursecode):
    # läs in alla uppgifter för coursecode och skicka till tasks.html
    try:
        course = course_ctrl.get_course_with_coursecode(coursecode)
        tasks = get_tasks_with_coursecode(coursecode)
        return template("tasks", course=course, tasks=tasks)

    except:
        return template("error")


@route("/<coursecode>/tasks/<id>")
def view_task(coursecode, id):
    # hämta uppgift med rätt id från uppgiftslistan och skicka till task.html
    try:
        course = course_ctrl.get_course_with_coursecode(coursecode)
        task = get_task_with_id(coursecode, id)
        return template("task", course=course, task=task)

    except:
        return template("error")


@route("/add-task", method="post")
def handle_add_task():
    return add_task_post()


@route("/<coursecode>/schedule")
def course_tasks(coursecode):
    # läs in alla tidsblock för coursecode och skicka till schedule.html
    try:
        course = course_ctrl.get_course_with_coursecode(coursecode)
        timeblocks = get_timeblocks_with_coursecode(coursecode)
        return template("schedule", course=course, timeblocks=timeblocks)

    except:
        return template("error")


@route("/<coursecode>/schedule/<id>")
def view_timeblock(coursecode, id):
    # hämta tidsblock med rätt id från tidsblocklistan och skicka till timeblock.html
    try:
        course = course_ctrl.get_course_with_coursecode(coursecode)
        timeblock = get_timeblock_with_id(coursecode, id)
        return template("timeblock", course=course, timeblock=timeblock)

    except:
        return template("error")


@route("/add-timeblock", method="post")
def handle_add_timeblock():
    return add_timeblock_post()


@route("/preferences")
def study_preferences():
    return template("studypreferences")


@route("/save-preferences", method="post")
def add_preferences():
    hours_per_week = getattr(request.forms, "rangeInput")
    # skriv till fil

    # flash message("Dina preferenser har sparats")
    redirect("/profile")

"""
@route("/profile")
def show_profile():
    return template("profile")


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
        all_events += filter_course_events()




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


def getnew():
    print("fem")


# Start our web server
run(host="127.0.0.1", port=8080, reloader=True)
