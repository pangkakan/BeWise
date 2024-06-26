from bottle import request, template, redirect
from models import courses, events
from models.json_manager import add_to_json, save_to_json_file, read_from_json_file


# def add_course_post(conn):
#     course_list = read_from_json_file("static/courses.json")
#     coursecode = request.forms.get("coursedropdown")

#     if courses.course_exists(course_list, coursecode):
#         print("Course already exists")
#         return template("addcourse")

#     # Construct course details based on coursecode
#     course = {"coursecode": coursecode.upper(), "title": ""}
#     if coursecode == "da336a":
#         course["title"] = "Systemutveckling och projekt"
#     elif coursecode == "da297a":
#         course["title"] = "Databasteknik"
#     elif coursecode == "da108a":
#         course["title"] = "Informationsarkitektur"

#     # Optionally retrieve and save timeblocks if part of the setup
#     if course["title"]:
#         course_events = events.get_events(
#             conn
#         )  # Assumes events model exists and has a method get_events()
#         for event in course_events:
#             event["coursecode"] = course["coursecode"]
#         save_to_json_file(course_events, "static/timeblocks.json")

#     add_to_json(course_list, course, "static/courses.json")
#     redirect("/")


# def add_course_post(conn):
#     coursecode = request.forms.get(course_code)

#     if courses.course_exists(course_list, coursecode):
#         print("Course already exists")
#         return template("addcourse")

#     # Construct course details based on coursecode
#     course = {"coursecode": coursecode.upper(), "title": ""}
#     if coursecode == "da336a":
#         course["title"] = "Systemutveckling och projekt"
#     elif coursecode == "da297a":
#         course["title"] = "Databasteknik"
#     elif coursecode == "da108a":
#         course["title"] = "Informationsarkitektur"

#     # Optionally retrieve and save timeblocks if part of the setup
#     if course["title"]:
#         course_events = events.get_events(
#             conn
#         )  # Assumes events model exists and has a method get_events()
        
        
#     redirect("/")


def get_course_with_coursecode(coursecode):
    courses = read_from_json_file("static/courses.json")
    for course in courses:
        if course["coursecode"] == coursecode:
            return course