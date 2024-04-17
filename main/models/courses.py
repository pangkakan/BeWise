from json_manager import save_to_json_file


def course_exists(courses, coursecode):
    return any(course["kurskod"] == coursecode.upper() for course in courses)

def add_course(courses, course_details):
    courses.append(course_details)
    save_to_json_file(courses, "static/courses.json")
