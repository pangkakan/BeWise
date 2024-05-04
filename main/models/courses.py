


def course_exists(courses, coursecode):
    return any(course["kurskod"] == coursecode.upper() for course in courses)

