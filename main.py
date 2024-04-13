from bottle import route, get, post, run, template, error, static_file, request, response, redirect
import json


# Läser från json-fil och returnerar lista av innehåll
def read_from_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
        
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Creating a new file.")
        with open(file_path, 'w') as file:
            json.dump([], file)
            return []
        
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{file_path}'.")
        return []
   

# Skriver lista av innehåll till json-fil
def save_to_json_file(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to '{file_path}' successfully.")

    except Exception as e:
        print(f"Error saving data to '{file_path}': {e}")




def get_course_with_coursecode(coursecode):
    courses = read_from_json_file("static/courses.json")
    for course in courses:
        if course["kurskod"] == coursecode:
            return course
        

def get_tasks_with_coursecode(coursecode):
    tasks = read_from_json_file("static/tasks.json")
    task_list = []
    for task in tasks:
        if task["kurskod"] == coursecode:
            task_list.append(task)
    
    return task_list


def get_timeblocks_with_coursecode(coursecode):
    timeblocks = read_from_json_file("static/timeblocks.json")
    timeblocks_list = []
    for timeblock in timeblocks:
        if timeblock["kurskod"] == coursecode:
            timeblocks_list.append(timeblock)
    
    return timeblocks_list











@route("/")
def index():
    # Lista av lexikon (kurs)
    courses = read_from_json_file("static/courses.json")    
    return template("mycourses", courses=courses)


@route("/<coursecode>")
def course_page(coursecode):
    # kontrollera att kurs med den kurskoden finns i courses.json
    try:
        course = get_course_with_coursecode(coursecode)
        return template("coursepage", course=course)
    except:
        return template("error")


@route("/new-course")
def new_course():
    return template("addcourse")


@route("/add-course", method="post")
def add_course():
    courses = read_from_json_file("static/courses.json")
    coursecode = getattr(request.forms, "coursedropdown")

    # kontrollera att kursen inte redan är tillagd
    for course in courses:
        if course["kurskod"] == coursecode.upper():
            print("Kursen finns redan")
            return template("addcourse")
    
    # skriv till courses.json
    course = {}

    if coursecode == "da336a":
        course["kurskod"] = "DA336A"
        course["titel"] = "Systemutveckling och projekt"
    elif coursecode == "da297a":
        course["kurskod"] = "DA297A"
        course["titel"] = "Databasteknik"
    elif coursecode == "da108a":
        course["kurskod"] = "DA108A"
        course["titel"] = "Informationsarkitektur"

    courses.append(course)
    save_to_json_file(courses, "static/courses.json")

    # flash message("Kursen har lagts till")
    redirect("/")


@route("/<coursecode>/tasks")
def course_tasks(coursecode):
    # läs in alla uppgifter för kurskod och skicka till tasks.html
    try:
        course = get_course_with_coursecode(coursecode)
        tasks = get_tasks_with_coursecode(coursecode)
        return template("tasks", course=course, tasks=tasks )
    
    except:
        return template("error")
    

@route("/<coursecode>/tasks/<id>")
def view_task():
    pass


@route("/add-task", method="post")
def add_task():
    # skriv till fil

    # flash message("Uppgiften har lagts till")
    pass


@route("/<coursecode>/schedule")
def course_tasks(coursecode):
    # läs in alla tidsblock för kurskod och skicka till schedule.html
    try:
        course = get_course_with_coursecode(coursecode)
        timeblocks = get_timeblocks_with_coursecode(coursecode)
        return template("schedule", course=course, timeblocks=timeblocks)
    
    except:
        return template("error")
    

@route("/<coursecode>/schedule/<id>")
def view_timeblock():
    pass


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