from bottle import request, template, redirect
from main.models import courses, events


def add_course_post(conn):
    course_list = courses.read_from_json_file("static/courses.json")
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
        course_events = events.get_events(conn)  # Assumes events model exists and has a method get_events()
        for event in course_events:
            event["kurskod"] = course["kurskod"]
        courses.save_to_json_file(course_events, "static/timeblocks.json")

    courses.add_course(course_list, course)
    redirect("/")
