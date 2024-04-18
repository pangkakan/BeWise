from bottle import request, redirect
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
        "kurskod": coursecode,
        "titel": timeblock_title,
        "datum": timeblock_date,
        "starttid": timeblock_start_time,
        "sluttid": timeblock_end_time,
    }


    add_to_json(all_timeblocks, new_timeblock, "static/timeblocks.json")



    # flash message("Tidsblocket har lagts till")
    # istället för redirect till startsidan kan detta lösas med htmx så man stannar kvar på sidan
    redirect("/")
