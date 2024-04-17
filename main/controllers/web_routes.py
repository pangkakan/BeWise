from bottle import route, template, request, redirect
from models import events, courses, tasks, timeblocks  # Import your model modules

@route("/")
def index():
    course_data = courses.read_from_json_file("static/courses.json")
    return template("mycourses", courses=course_data)