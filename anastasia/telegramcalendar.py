import telegram
import calendar

def create_calendar(year,month):
    #First row - Month and Year
    rows=[]
    row =[]
    row.append(telegram.InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data="ignore"))
    rows.append(row)
    #Second row - Week Days
    week_days=["L","M","M","J","V","S","D"]
    row=[]
    for day in week_days:
        row.append(telegram.InlineKeyboardButton(day,callback_data="ignore"))
    rows.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(telegram.InlineKeyboardButton(" ",callback_data="ignore"))
            else:
                row.append(telegram.InlineKeyboardButton(str(day),callback_data="calendar-day-"+str(day)))
        rows.append(row)
    #Last row - Buttons
    row=[]
    row.append(telegram.InlineKeyboardButton("<",callback_data="previous-month"))
    row.append(telegram.InlineKeyboardButton(" ",callback_data="ignore"))
    row.append(telegram.InlineKeyboardButton(">",callback_data="next-month"))
    rows.append(row)
    markup = telegram.InlineKeyboardMarkup(rows)
    return markup

