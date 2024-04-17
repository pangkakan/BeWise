from bottle import route, get, post, run, template, error, static_file, request, response, redirect
import json
import psycopg2
from controllers.db import create_connection
from main.controllers import course_controller as course_ctrl
from datetime import datetime

from main.mainTing.scraper import Scraper
from models.courses import read_from_json_file, save_to_json_file

conn = create_connection()




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


def get_task_with_id(coursecode, id):
    tasks = get_tasks_with_coursecode(coursecode)
    for task in tasks:
        if task["id"] == int(id):
            return task


def get_timeblocks_with_coursecode(coursecode):
    timeblocks = read_from_json_file("static/timeblocks.json")
    timeblocks_list = []
    for timeblock in timeblocks:
        if timeblock["kurskod"] == coursecode:
            timeblocks_list.append(timeblock)
    
    return timeblocks_list


def get_timeblock_with_id(coursecode, id):
    timeblocks = get_timeblocks_with_coursecode(coursecode)
    for timeblock in timeblocks:
        if timeblock["id"] == int(id):
            return timeblock


# Generell funktion som tar emot listor av lexikon där man utgår från att alla lexikon har id-nyckel
def create_id(list_of_dictionaries):
    highest_id = 1
    for dictionary in list_of_dictionaries:
        if dictionary["id"] >= highest_id:
            highest_id = dictionary["id"] + 1
    return highest_id








@route("/")
def index():
    # Lista av kurser
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
    return course_ctrl.add_course_post(conn)


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
def view_task(coursecode, id):
    # hämta uppgift med rätt id från uppgiftslistan och skicka till task.html
    try:
        course = get_course_with_coursecode(coursecode)
        task = get_task_with_id(coursecode, id)
        return template("task", course=course, task=task)
    
    except:
        return template("error")


@route("/add-task", method="post")
def add_task():
    coursecode = getattr(request.forms, "coursecode")
    task_title = getattr(request.forms, "task_title")
    task_date = getattr(request.forms, "task_date")

    # hämta alla inlagda uppgifter
    all_tasks = read_from_json_file("static/tasks.json")
    # skapa unikt id för uppgift
    task_id = create_id(all_tasks)

    new_task = {
        "id": task_id,
        "kurskod": coursecode,
        "titel": task_title,
        "datum": task_date
    }
    # lägg till den nya uppgiften i uppgiftslistan
    all_tasks.append(new_task)

    # skriv till tasks.json
    save_to_json_file(all_tasks, "static/tasks.json")


    # flash message("Uppgiften har lagts till")
    # istället för redirect till startsidan kan detta lösas med htmx så man stannar kvar på sidan
    redirect("/")


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
def view_timeblock(coursecode, id):
    # hämta tidsblock med rätt id från tidsblocklistan och skicka till timeblock.html
    try:
        course = get_course_with_coursecode(coursecode)
        timeblock = get_timeblock_with_id(coursecode, id)
        return template("timeblock", course=course, timeblock=timeblock)
            
    except:
        return template("error")


@route("/add-timeblock", method="post")
def add_timeblock():
    coursecode = getattr(request.forms, "coursecode")
    timeblock_title = getattr(request.forms, "timeblock_title")
    timeblock_date = getattr(request.forms, "timeblock_date")
    timeblock_start_time = getattr(request.forms, "timeblock_start_time")
    timeblock_end_time = getattr(request.forms, "timeblock_end_time")

    # hämta alla inlagda tidsblock
    all_timeblocks = read_from_json_file("static/timeblocks.json")
    # skapa unikt id för uppgift
    timeblock_id = create_id(all_timeblocks)

    new_timeblock = {
        "id": timeblock_id,
        "kurskod": coursecode,
        "titel": timeblock_title,
        "datum": timeblock_date,
        "starttid": timeblock_start_time,
        "sluttid": timeblock_end_time
    }
    # lägg till den nya uppgiften i uppgiftslistan
    all_timeblocks.append(new_timeblock)

    # skriv till timeblocks.json
    save_to_json_file(all_timeblocks, "static/timeblocks.json")


    # flash message("Tidsblocket har lagts till")
    # istället för redirect till startsidan kan detta lösas med htmx så man stannar kvar på sidan
    redirect("/")


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

