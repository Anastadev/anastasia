#!/usr/bin/python3
from datetime import datetime
import mysql.connector as mariadb
from loghelper import log
from confighelper import ConfigHelper
import sys

conf = ConfigHelper(sys.argv[1])

mariadb_connection = mariadb.connect(user=conf.get_db_user(), password=conf.get_db_pass(), database=conf.get_db_name())
cursor = mariadb_connection.cursor()


def usage():
    return "/todo list all todo\n" \
           "/todo [-a %m%d%H task] add a todo (example : /todo -a 251200 kdo)\n" \
           "/todo [-d id] delete a todo"


def cleanList():
    cursor.execute("DELETE FROM todolist WHERE end_date < now()")
    cursor.execute("COMMIT WORK")


def alltodolist(chat_id):
    cleanList()
    cursor.execute("SELECT id, end_date, task FROM todolist WHERE chat_id = %s ORDER BY end_date", (chat_id,))
    string = ""

    for id, end_date, task in cursor:
        string += str(end_date.strftime("%d/%m %H")) + " H (" + str(id) + ") : " + task + "\n"

    return string


def deleteTodo(chat_id, id):
    cursor.execute("DELETE FROM todolist WHERE id = %s AND chat_id = %s", (id, chat_id))
    cursor.execute("COMMIT WORK")


def addTodo(chat_id, date, task):
    cursor.execute("INSERT INTO todolist(chat_id,end_date,task) VALUES(%s,%s,%s)", (chat_id, date, task))
    cursor.execute("commit work")


def give_todo(bot, update, args):
    if len(args) == 0:
        log.info("Give the todolist")
        bot.sendMessage(chat_id=update.message.chat_id, text=alltodolist(update.message.chat_id))
    elif len(args) >= 3 and args[0] == "-a":
        try:
            d = datetime.strptime(args[1], '%d%m%H')
            y = datetime.now().year
            if d.month < datetime.now().month:
                y += 1
            d = d.replace(year=y)
            addTodo(update.message.chat_id, d, ' '.join(args[2:]))
        except:
            log.info("bad date format")
            bot.sendMessage(chat_id=update.message.chat_id, text=usage())
            pass
            return
        log.info("Add to the todolist")
    elif len(args) == 2 and args[0] == "-d":
        log.info("Delete " + args[1] + " to the todolist")
        deleteTodo(update.message.chat_id, args[1])
    else:
        log.info("Bad format command")
        bot.sendMessage(chat_id=update.message.chat_id, text=usage())
