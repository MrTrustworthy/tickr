#!/usr/bin/env python3.3
# -*- coding: utf8 -*-
__author__ = 'MrTrustworthy'

import sqlite3
from datetime import datetime
from functools import wraps
from operator import attrgetter
import os

# Database names/folders
LINUX_FOLDER_PREFIX = os.path.expanduser('~') + '/html/tickr/'
DB_URI = LINUX_FOLDER_PREFIX + "example.db"

# For windows
if os.name == "nt":
    DB_URI = "C:\\Users\\mt\\Desktop\\tickr\\example.db"


# WRAPS

def with_cursor(wrapped_func):
    @wraps(wrapped_func)
    def wrap(*args, **kwargs):
        print(DB_URI)
        with sqlite3.connect(DB_URI) as connection:
            cursor = connection.cursor()
            return wrapped_func(cursor, *args, **kwargs)

    return wrap


# somecomment
@with_cursor
def setup_db(cursor):
    # Create table
    cursor.execute('''CREATE TABLE tickets
	             (
	             	ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
	             	name text, 
	             	date text, 
	             	state text,
	             	deadline text
	             	)''')

    cursor.execute('''CREATE TABLE comments
	             (
	             	comment_id INTEGER PRIMARY KEY AUTOINCREMENT, 
	             	content text, 
	             	date text,
	             	ticket_id INTEGER, FOREIGN KEY(ticket_id) REFERENCES tickets(ticket_id)
	             	)''')

    print("done!")


@with_cursor
def alter_table(cursor):
    cursor.execute("ALTER TABLE tickets ADD COLUMN deadline text")


"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""



#somecomment
@with_cursor
def add_ticket(cursor, name):
    time = str(datetime.now())
    cursor.execute("INSERT INTO tickets VALUES (null, ?,?,?, 'None')", [name, time, "OPEN"])


#somecomment
@with_cursor
def change_state(cursor, ticket_id, new_state):
    cursor.execute("UPDATE tickets SET state = ? WHERE ticket_id = ?", [new_state, ticket_id])

#somecomment
@with_cursor
def change_deadline(cursor, ticket_id, new_deadline):
    cursor.execute("UPDATE tickets SET deadline = ? WHERE ticket_id = ?", [new_deadline, ticket_id])


#somecomment
@with_cursor
def add_comment(cursor, ticket_id, comment):
    time = str(datetime.now())
    cursor.execute("INSERT INTO comments VALUES (null, ?, ?, ?)", [comment, time, ticket_id])


@with_cursor
def get_all(cursor, state):
    cursor.execute("SELECT * FROM tickets")

    tickets = cursor.fetchall()

    cursor.execute("SELECT * FROM comments")

    comments = cursor.fetchall()

    #date sort function
    def sort_by_date(item):
        return item["date"]

    def sort_by_deadline(item):
        return str(item["deadline"])

    #we put them all in here
    formatted_tickets = [];

    #reformat
    for ticket in tickets:

        if ticket[3] == state:
            formatted_ticket = {
                "id": ticket[0],
                "name": ticket[1],
                "date": ticket[2][:19],
                "state": ticket[3],
                "deadline": ticket[4],
                "comments": [
                    {
                        "date": comment[2][:19],
                        "content": comment[1]  #for every fitting comment
                    } for comment in comments if comment[3] == ticket[0]]

            }
            formatted_ticket["comments"].sort(key=sort_by_date, reverse=True)

            formatted_tickets.append(formatted_ticket)

    formatted_tickets.sort(key=sort_by_deadline)

    return formatted_tickets


if __name__ == "__main__":
    setup_db();
    #alter_table()