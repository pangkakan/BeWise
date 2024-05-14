import json

from bottle import route, run, template, error, static_file, request, redirect, response
from controllers import course_controller as course_ctrl
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
from models.json_manager import read_from_json_file

conn = create_connection()


@route("/")
def index():
    # Lista av kurser
    # fem
    courses = read_from_json_file("static/courses.json")
    return template("mycourses", courses=courses)


@route("/<coursecode>")
def course_page(coursecode):
    # kontrollera att kurs med den kurskoden finns i courses.json
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
    # läs in alla uppgifter för kurskod och skicka till tasks.html
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
    # läs in alla tidsblock för kurskod och skicka till schedule.html
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


@route("/profile")
def show_profile():
    return template("profile")


@route("/api/calendar")
def calendar_api():
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
                "kurskod": event["kurskod"]
            }
        }
        formatted_events.append(formatted_event)

    # Return the formatted events
    response.content_type = 'application/json'
    return json.dumps(formatted_events)

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
