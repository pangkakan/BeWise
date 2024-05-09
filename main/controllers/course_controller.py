from bottle import request, template, redirect
from models import courses, events
from models.json_manager import add_to_json, save_to_json_file, read_from_json_file


def add_course_post(conn):
    course_list = read_from_json_file("./main/static/courses.json")
    coursecode = request.forms.get("coursedropdown")

    if courses.course_exists(course_list, coursecode):
        print("Course already exists")
        return template("addcourse")

    # Construct course details based on coursecode
    course = {"kurskod": coursecode.upper(), "titel": ""}
    if coursecode == "da336a":
        course["titel"] = "Systemutveckling och projekt"
    elif coursecode == "da297a":
        course["titel"] = "Databasteknik"
    elif coursecode == "da108a":
        course["titel"] = "Informationsarkitektur"

    # Optionally retrieve and save timeblocks if part of the setup
    if course["titel"]:
        courses.add_course(conn, '2024-01-01', '2024-12-31', course["kurskod"], course["titel"])
        events.scrape_to_db(conn, course["kurskod"], True)
        course_events = events.get_events(
            conn
        )  # Assumes events model exists and has a method get_events()
        for event in course_events:
            event["kurskod"] = course["kurskod"]
        save_to_json_file(course_events, "./main/static/timeblocks.json")

    add_to_json(course_list, course, "./main/static/courses.json")
    redirect("/")


def get_course_with_coursecode(coursecode):
    courses = read_from_json_file("./main/static/courses.json")
    for course in courses:
        if course["kurskod"] == coursecode:
            return course
