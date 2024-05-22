from bottle import request, redirect
from models.json_manager import read_from_json_file, save_to_json_file
from models.shared import create_id


def add_task_post(conn):
    coursecode = getattr(request.forms, "coursecode")
    task_title = getattr(request.forms, "task_title")
    task_date = getattr(request.forms, "task_date")

    # hämta alla inlagda uppgifter
    all_tasks = read_from_json_file("static/tasks.json")
    # skapa unikt id för uppgift
    task_id = create_id(all_tasks)

    new_task = {
        "id": task_id,
        "coursecode": coursecode,
        "title": task_title,
        "datum": task_date,
    }
    # lägg till den nya uppgiften i uppgiftslistan
    all_tasks.append(new_task)

    # skriv till tasks.json
    save_to_json_file(all_tasks, "static/tasks.json")

    # flash message("Uppgiften har lagts till")
    # istället för redirect till startsidan kan detta lösas med htmx så man stannar kvar på sidan
    redirect("/")


    

    


    


def get_tasks_with_coursecode(coursecode):
    tasks = read_from_json_file("static/tasks.json")
    task_list = []
    for task in tasks:
        if task["coursecode"] == coursecode:
            task_list.append(task)

    return task_list


def get_task_with_id(coursecode, id):
    tasks = get_tasks_with_coursecode(coursecode)
    for task in tasks:
        if task["id"] == int(id):
            return task