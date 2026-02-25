import re
from datetime import datetime

from anastasia.telegramcalendar import create_calendar

from anastasia.loghelper import log
from anastasia.storage import TodoStore
from telegram import Update
from telegram.ext import ContextTypes


class Todo:
    # contains the month printed by addtodo and the self.todos content
    def __init__(self):
        self.current_shown_dates = {}
        self.store = TodoStore()

    @staticmethod
    def usage():
        return "/todo list all todo\n" \
               "/todo [-d id] delete a todo"

    def clean_list(self,chat_id):
        self.store.cleanup_expired(chat_id)

    def all_to_do_list(self, chat_id):
        self.clean_list(chat_id)
        st = ""
        ct = 1
        for todo in self.store.list(chat_id):
            st += str(todo.date.strftime("%d/%m")) + " (" + str(ct) + ") : " + todo.task + "\n"
            ct += 1
        return st

    def delete_todo(self, chat_id, id_todo):
        try:
            idx = int(id_todo)
        except Exception:
            return
        self.store.delete_by_list_index(chat_id, idx)

    def add_todo(self, chat_id, message_id, date, task):
        todo = self.store.add(chat_id=chat_id, date=date, task=task)
        log.info("insert id : " + str(todo.id))
        return todo

    async def give_add_todo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        now = datetime.now()  # Current date
        if not update.message:
            return
        chat_id = update.message.chat.id
        date = (now.year, now.month)
        self.current_shown_dates[chat_id] = [date, ' '.join(context.args)]  # Saving the current date in a dict
        markup = create_calendar(now.year, now.month)
        await update.message.reply_text("Choisir une date", reply_markup=markup)

    async def todo_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.callback_query:
            return
        if update.callback_query.data == "next-month":
            await self.next_month(update, context)
        elif update.callback_query.data == "previous-month":
            await self.previous_month(update, context)
        elif update.callback_query.data == "ignore":
            await update.callback_query.answer(text="")
        else:
            await self.choose_day(update, context)

    async def choose_day(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.callback_query:
            return
        ma = re.match("calendar-day-([0-9]+)", update.callback_query.data or "")
        if ma is not None:
            chat_id = update.callback_query.message.chat.id
            date = datetime.strptime(
                str(self.current_shown_dates[chat_id][0][0]) + str(self.current_shown_dates[chat_id][0][1]),
                '%Y%m').replace(day=int(ma.group(1)))
            todo = self.add_todo(
                update.callback_query.message.chat_id,
                update.callback_query.message.message_id,
                date,
                self.current_shown_dates[chat_id][1],
            )
            log.info("add todo : " + str(todo))
            await update.callback_query.edit_message_text(
                f"{todo.date.strftime('%d/%m')} : {todo.task}",
                reply_markup=None,
            )

    async def previous_month(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.callback_query:
            return
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
            await update.callback_query.edit_message_text("Choisir une date", reply_markup=markup)
            await update.callback_query.answer(text="")
        else:
            # Do something to inform of the error
            pass

    async def next_month(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.callback_query:
            return
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
            await update.callback_query.edit_message_text("Please, choose a date", reply_markup=markup)
            await update.callback_query.answer(text="")
        else:
            # Do something to inform of the error
            pass

    async def give_todo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message:
            return
        if len(context.args) == 0:
            log.info("Give the todolist")
            await update.message.reply_text(self.all_to_do_list(update.message.chat_id))
        elif len(context.args) == 2 and context.args[0] == "-d":
            log.info("Delete " + context.args[1] + " to the todolist")
            self.delete_todo(update.message.chat_id, context.args[1])
        else:
            log.info("Bad format command")
            await update.message.reply_text(self.usage())
