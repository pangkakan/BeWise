


def course_exists(courses, coursecode):
    return any(course["kurskod"] == coursecode.upper() for course in courses)


def add_course(conn, start_time, end_time, coursecode, title):
    cur = conn.cursor()

    #cur.execute("DELETE FROM courses")
    cur.execute("INSERT INTO courses (start_timestamp, end_timestamp, course_code, title) VALUES (%s, %s, %s, %s)", (start_time, end_time, coursecode, title,))

    conn.commit()



