from bottle import request, redirect, template
from controllers.course_controller import get_course_with_coursecode
from models.json_manager import read_from_json_file, save_to_json_file
from models.shared import create_id
from models.json_manager import add_to_json


def add_timeblock_post():
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
        "coursecode": coursecode,
        "title": timeblock_title,
        "datum": timeblock_date,
        "starttid": timeblock_start_time,
        "sluttid": timeblock_end_time,
    }


    add_to_json(all_timeblocks, new_timeblock, "static/timeblocks.json")



    # flash message("Tidsblocket har lagts till")
    # istället för redirect till startsidan kan detta lösas med htmx så man stannar kvar på sidan
    redirect("/")

def view_timeblock(coursecode, id):
    # hämta tidsblock med rätt id från tidsblocklistan och skicka till timeblock.html
    try:
        course = get_course_with_coursecode(coursecode)
        timeblock = get_timeblock_with_id(coursecode, id)
        return template("timeblock", course=course, timeblock=timeblock)

    except:
        return template("error")

def get_timeblock_with_id(coursecode, id):
    timeblocks = get_timeblocks_with_coursecode(coursecode)
    for timeblock in timeblocks:
        if timeblock["id"] == int(id):
            return timeblock

def get_timeblocks_with_coursecode(coursecode):
    timeblocks = read_from_json_file("static/timeblocks.json")
    timeblocks_list = []
    for timeblock in timeblocks:
        if timeblock["coursecode"] == coursecode:
            timeblocks_list.append(timeblock)

    return timeblocks_list


