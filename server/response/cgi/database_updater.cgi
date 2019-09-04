#!/usr/local/bin/python3

import mysql.connector


def get_running_status(cursor):
    query = cursor.execute(
        "SELECT status FROM status WHERE label='running';")

    result = None
    try:
        result = [i[0] for i in cursor][0]
    except TypeError:
        return result

    return result is 1


def get_current_position(cursor):
    query = cursor.execute(
        "SELECT status FROM status WHERE label='position';")

    result = None
    try:
        result = [i[0] for i in cursor][0]
    except TypeError:
        return result

    return result


def get_info(cursor):
    running_answer = get_running_status(cursor)
    current_position = get_current_position(cursor)
    return running_answer, current_position


def display_info(running_answer, current_position):
    # Required header that tells the browser how to render the text.
    print("Content-Type: text/plain\n\n")  # here text -- not html

    # Print a simple message to the display window.
    print("Irrigation Program Information:\n")
    print("  - Running: {}".format(running_answer))
    print("  - Current position: {}".format(current_position))


def run():
    db = mysql.connector.connect(
        host="localhost",
        user="irrigation_program",
        passwd="1234",
        database="irrigation_db"
    )

    cursor = db.cursor()

    running_answer, current_position= get_info(cursor)
    display_info(running_answer, current_position)


run()
