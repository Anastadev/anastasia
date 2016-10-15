#!/usr/bin/python3
import mysql.connector as mariadb
import time

mariadb_connection = mariadb.connect(user='todolistuser', password='todolistpass', database='todolist')
cursor = mariadb_connection.cursor()

# cursor.execute("insert into todolist(end_date,task) VALUES(%s,%s)",(time.strftime('%Y/%m/%d %H:00:00'),"test"))
# cursor.execute("commit work")

def usage():
    return  "/todo list all todo\n" \
            "/todo [-a %m%d%H task] add a todo\n" \
            "/todo [-d id] delete a todo"

def alltodolist():

    cursor.execute("SELECT id, end_date, task FROM todolist ORDER BY end_date")
    string = ""
    for id, end_date, task in cursor:
        string += str(end_date.strftime("%Y/%m/%d %H")) +" H ("+str(id)+") : " + task+"\n"

    return string

