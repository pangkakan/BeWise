


def course_exists(courses, coursecode):
    return any(course["coursecode"] == coursecode.upper() for course in courses)

