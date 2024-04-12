from bottle import route, get, post, run, template, error, static_file, request, response, redirect
import json


@route("/")
def index():
    # läs från fil
    
    return template("mycourses")


@route("/<coursecode>")
def course_page(coursecode):
    return template("coursepage", coursecode=coursecode)


@route("/new-course")
def new_course():
    return template("addcourse")


@route("/add-course", method="post")
def add_course():
    courseCode = getattr(request.forms, "coursedropdown")
    # skriv till fil...

    # flash message("Kursen har lagts till")
    redirect("/")


@route("/<coursecode>/tasks")
def course_tasks(coursecode):
    return template("tasks", coursecode=coursecode)


@route("/add-task", method="post")
def add_task():
    # skriv till fil

    # flash message("Uppgiften har lagts till")
    pass


@route("/<coursecode>/schedule")
def course_tasks(coursecode):
    return template("schedule", coursecode=coursecode)


@route("/add-timeblock", method="post")
def add_timeblock():
    # skriv till fil

    # flash message("Tidsblocket har lagts till")
    pass


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


















@error(404)
def error404(error):
    '''
    Visar felmeddelande för sida som ej existerar

    Returnerar error.html
    '''
    return template("error")


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