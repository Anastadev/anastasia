import re
import sys
from datetime import datetime

from anastasia.confighelper import ConfigHelper
from pymongo import MongoClient
from anastasia.telegramcalendar import create_calendar

from anastasia.loghelper import log


class Todo:
    # contains the month printed by addtodo and the self.todos content
    def __init__(self):
        self.current_shown_dates = {}

        conf = ConfigHelper(sys.argv[1])

        client = MongoClient(conf.get_db())
        db = client[conf.get_db_name()]
        self.todos = db.self.todos

    @staticmethod
    def usage():
        return "/todo list all todo\n" \
               "/todo [-d id] delete a todo"

    def clean_list(self):
        self.todos.remove({"date": {"$lt": datetime.now()}})

    def all_to_do_list(self, chat_id):
        self.clean_list()
        st = ""
        ct = 1
        for todo in self.todos.find({"chat_id": chat_id}).sort("date"):
            st += str(todo["date"].strftime("%d/%m")) + " (" + str(ct) + ") : " + todo["task"] + "\n"
            ct += 1
        return st

    def delete_todo(self, chat_id, id_todo):
        self.todos.remove(self.todos.find({"chat_id": chat_id}).sort("date")[int(id_todo) - 1])

    def add_todo(self, chat_id, date, task):
        todo = {
            "chat_id": chat_id,
            "task": task,
            "date": date
        }
        id_todo = self.todos.insert_one(todo)
        log.info("insert id : " + str(id_todo))
        return todo

    def give_add_todo(self, bot, update, args):
        now = datetime.now()  # Current date
        chat_id = update.message.chat.id
        date = (now.year, now.month)
        self.current_shown_dates[chat_id] = [date, ' '.join(args)]  # Saving the current date in a dict
        markup = create_calendar(now.year, now.month)
        bot.send_message(update.message.chat.id, "Choisir une date", reply_markup=markup)

    def todo_callback(self, bot, update):
        if update.callback_query.data == "next-month":
            self.next_month(bot, update)
        elif update.callback_query.data == "previous-month":
            self.previous_month(bot, update)
        elif update.callback_query.data == "ignore":
            bot.answer_callback_query(update.callback_query.id, text="")
        else:
            self.choose_day(bot, update)

    def choose_day(self, bot, update):
        ma = re.match("calendar-day-([0-9]+)", update.callback_query.data)
        if ma is not None:
            chat_id = update.callback_query.message.chat.id
            date = datetime.strptime(
                str(self.current_shown_dates[chat_id][0][0]) + str(self.current_shown_dates[chat_id][0][1]),
                '%Y%m').replace(day=int(ma.group(1)))
            todo = self.add_todo(chat_id, date, self.current_shown_dates[chat_id][1])
            log.info("add todo : " + str(todo))
            bot.edit_message_text(str(todo["date"].strftime("%d/%m")) + " : " + todo["task"],
                                  update.callback_query.from_user.id, update.callback_query.message.message_id,
                                  reply_markup="")

    def previous_month(self, bot, update):
        chat_id = update.callback_query.message.chat.id
        saved_date = self.current_shown_dates.get(chat_id)[0]
        if saved_date is not None:
            year, month = saved_date
            month -= 1
            if month < 1:
                month = 12
                year -= 1
            date = (year, month)
            self.current_shown_dates[chat_id][0] = date
            markup = create_calendar(year, month)
            bot.edit_message_text("Choisir une date", update.callback_query.from_user.id,
                                  update.callback_query.message.message_id, reply_markup=markup)
            bot.answer_callback_query(update.callback_query.id, text="")
        else:
            # Do something to inform of the error
            pass

    def next_month(self, bot, update):
        chat_id = update.callback_query.message.chat.id
        saved_date = self.current_shown_dates.get(chat_id)[0]
        if saved_date is not None:
            year, month = saved_date
            month += 1
            if month > 12:
                month = 1
                year += 1
            date = (year, month)
            self.current_shown_dates[chat_id][0] = date
            markup = create_calendar(year, month)
            bot.edit_message_text("Please, choose a date", update.callback_query.from_user.id,
                                  update.callback_query.message.message_id, reply_markup=markup)
            bot.answer_callback_query(update.callback_query.id, text="")
        else:
            # Do something to inform of the error
            pass

    def give_todo(self, bot, update, args):
        if len(args) == 0:
            log.info("Give the todolist")
            bot.sendMessage(chat_id=update.message.chat_id, text=self.all_to_do_list(update.message.chat_id))
        elif len(args) == 2 and args[0] == "-d":
            log.info("Delete " + args[1] + " to the todolist")
            self.delete_todo(update.message.chat_id, args[1])
        else:
            log.info("Bad format command")
            bot.sendMessage(chat_id=update.message.chat_id, text=self.usage())
