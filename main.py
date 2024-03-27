from bottle import run, template, route, request, redirect, static_file
import json

@route("/")
def index():
    return template("index")


@route("/schedule")
def schedule():
    return template("schedule")


@route("/importantdates")
def schedule():
    return template("importantdates")


@route("/tasks")
def schedule():
    return template("tasks")


@route("/add-course", method="post")
def add_course():
    courseCode = getattr(request.forms, "courseCode")
    return template("mycourses", courseCode=courseCode)


@route("/static/<filename>")
def static_files(filename):
    '''
    Handles the routes to our static files
	
	Returns:
		file : the static file requested by URL	
	'''
    return static_file(filename, root="static")


# Start our web server
run(host="127.0.0.1", port=8080, reloader=True)