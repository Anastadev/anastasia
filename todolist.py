#!/usr/bin/python3
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='todolistuser', password='todolistpass', database='todolist')
cursor = mariadb_connection.cursor()


def usage():
    return "/todo list all todo\n" \
           "/todo [-a %m%d%H task] add a todo (example : /todo -a 251200 kdo)\n" \
           "/todo [-d id] delete a todo"


def cleanList():
    cursor.execute("DELETE FROM todolist WHERE end_date < now()")
    cursor.execute("COMMIT WORK")


def alltodolist():
    cleanList()
    cursor.execute("SELECT id, end_date, task FROM todolist ORDER BY end_date")
    string = ""

    for id, end_date, task in cursor:
        string += str(end_date.strftime("%d/%m %H")) + " H (" + str(id) + ") : " + task + "\n"

    return string


def deleteTodo(id):
    cursor.execute("DELETE FROM todolist WHERE id = %s", (id,))
    cursor.execute("COMMIT WORK")


def addTodo(date, task):
    cursor.execute("INSERT INTO todolist(end_date,task) VALUES(%s,%s)", (date, task))
    cursor.execute("commit work")
