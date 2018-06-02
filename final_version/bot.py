from telebot import types

import telebot
import time

import datetime
from telegramcalendar import create_calendar

current_shown_dates={}

bot = telebot.TeleBot("520114385:AAHcTFjWOH5-zzID9GYyMEcQNIuFdQe2MVU")

general_information_past = open("general_information_past.txt", 'r')
general_information_ongoing = open("general_information_ongoing.txt", 'r')
general_information_upcoming = open("general_information_upcoming.txt", 'r')
name_ongoing = open("ongoing_ico_name.txt", 'r')
date_ongoing = open("ongoing_dates.txt", 'r')
other_ongoing = open("ongoing_other.txt", 'r')
o_date = date_ongoing.readlines()
o_name = name_ongoing.readlines()
o_other = other_ongoing.readlines()
p_info = general_information_past.readlines()
o_info = general_information_ongoing.readlines()
u_info = general_information_upcoming.readlines()

o_by_date = []

def pages_keyboard(start, stop, m):
    if m == 'Ongoing':
        keyboard = types.InlineKeyboardMarkup()
        btns = []
        if start > 0: btns.append(types.InlineKeyboardButton(
            text='⬅', callback_data= m + '+{}'.format(start - 5)))
        btns.append(types.InlineKeyboardButton(
            text=str(start // 5 + 1), callback_data = 'page+0'))
        if stop < len(o_info): btns.append(types.InlineKeyboardButton(
            text='➡', callback_data= m + '+{}'.format(stop)))
        keyboard.add(*btns)
        return keyboard
    if m == 'Past':
        keyboard = types.InlineKeyboardMarkup()
        btns = []
        if start > 0: btns.append(types.InlineKeyboardButton(
            text='⬅', callback_data=m + '+{}'.format(start - 5)))
        btns.append(types.InlineKeyboardButton(
            text=str(start // 5 + 1), callback_data='page+0'))
        if stop < len(p_info): btns.append(types.InlineKeyboardButton(
            text='➡', callback_data=m + '+{}'.format(stop)))
        keyboard.add(*btns)
        return keyboard
    if m == 'Upcoming':
        keyboard = types.InlineKeyboardMarkup()
        btns = []
        if start > 0: btns.append(types.InlineKeyboardButton(
            text='⬅', callback_data=m + '+{}'.format(start - 5)))
        btns.append(types.InlineKeyboardButton(
            text=str(start // 5 + 1), callback_data='page+0'))
        if stop < len(u_info): btns.append(types.InlineKeyboardButton(
            text='➡', callback_data=m + '+{}'.format(stop)))
        keyboard.add(*btns)
        return keyboard
    if m == 'Ongoing by date':
        keyboard = types.InlineKeyboardMarkup()
        btns = []
        if start > 0: btns.append(types.InlineKeyboardButton(
            text='⬅', callback_data=m + '+{}'.format(start - 5)))
        btns.append(types.InlineKeyboardButton(
            text=str(start // 5 + 1), callback_data='page+0'))
        if stop < len(o_by_date): btns.append(types.InlineKeyboardButton(
            text='➡', callback_data=m + '+{}'.format(stop)))
        keyboard.add(*btns)
        return keyboard

@bot.message_handler(commands=['start'])
def start(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Past', 'Ongoing', 'Upcoming', 'Ongoing by date']])
    msg = bot.send_message(m.chat.id, 'Choose time period', reply_markup=keyboard)
    bot.register_next_step_handler(msg, name)

def name(m):
    if m.text == 'Past':
        bot.send_message(
            m.chat.id,
            '_' + '\n'.join(map(str, p_info[:5])) + '_',
            parse_mode='Markdown',
            reply_markup=pages_keyboard(0, 5, m.text))
    elif m.text == 'Ongoing':
        bot.send_message(
            m.chat.id,
            '_' + '\n'.join(map(str, o_info[:5])) + '_',
            parse_mode='Markdown',
            reply_markup=pages_keyboard(0, 5, m.text))
    elif m.text == 'Upcoming':
        bot.send_message(
            m.chat.id,
            '_' + '\n'.join(map(str, u_info[:5])) + '_',
            parse_mode='Markdown',
            reply_markup=pages_keyboard(0, 5, m.text))
    elif m.text == 'Ongoing by date':
        now = datetime.datetime.now()
        chat_id = m.chat.id
        date = (now.year, now.month)
        current_shown_dates[chat_id] = date
        markup = create_calendar(now.year, now.month)
        bot.send_message(m.chat.id, "Please, choose a date", reply_markup=markup)
    if m.text in ['Past', 'Ongoing', 'Upcoming']:
        msg1 = bot.send_message(m.chat.id, 'Table provides information about /ICO name/date/hype score/risk score/goal/')
        bot.register_next_step_handler(msg1, name)
    else:
        msg1 = bot.send_message(m.chat.id, 'Chosen date is:')
        bot.register_next_step_handler(msg1, name)

@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        pass

@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day=call.data[13:]
        date = datetime.datetime(int(saved_date[0]),int(saved_date[1]),int(day),0,0,0)
        d, tmp = str(date).split(' ')
        bot.send_message(chat_id, str(d))
        year, month, day = map(int, str(d).split('-'))
        o_by_date.clear()
        for i in range(len(o_date)):
            start, end = map(str, o_date[i].rstrip().split('-'))
            start_list = list(map(int, start.split('.')))
            end_list = list(map(int, end.split('.')))
            if start_list[2] < year or (start_list[2] == year and start_list[1] < month) or (
                        start_list[2] == year and start_list[1] == month and start_list[0] <= day):
                if end_list[2] > year or (end_list[2] == year and end_list[1] > month) or (
                            end_list[2] == year and end_list[1] == month and end_list[0] >= day):
                    o_by_date.append(o_name[i].rstrip() + " " + o_date[i].rstrip() + " " + o_other[i].rstrip() + "\n")
        if len(o_by_date) == 0:
            bot.send_message(chat_id, "Not found")
            bot.answer_callback_query(call.id, text="")
        else:
            bot.send_message(
                call.message.chat.id,
                '_' + '\n'.join(map(str, o_by_date[:5])) + '_',
                parse_mode='Markdown',
                reply_markup=pages_keyboard(0, 5, 'Ongoing by date'))
            bot.answer_callback_query(call.id, text="")

    else:
        pass

@bot.callback_query_handler(func=lambda c: c.data)
def pages(c):
    try:
        m, c.data = c.data.split('+')
        if m == 'Ongoing':
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text = '_' + '\n'.join(map(str, o_info[int(c.data[:]):int(c.data[:]) + 5])) + '_',
                parse_mode='Markdown',
                reply_markup=pages_keyboard(int(c.data[:]), int(c.data[:]) + 5, m))
        elif m == 'Upcoming':
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text='_' + '\n'.join(map(str, u_info[int(c.data[:]):int(c.data[:]) + 5])) + '_',
                parse_mode='Markdown',
                reply_markup=pages_keyboard(int(c.data[:]), int(c.data[:]) + 5, m))
        elif m == 'Past':
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text='_' + '\n'.join(map(str, p_info[int(c.data[:]):int(c.data[:]) + 5])) + '_',
                parse_mode='Markdown',
                reply_markup=pages_keyboard(int(c.data[:]), int(c.data[:]) + 5, m))
        elif m == 'Ongoing by date':
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text='_' + '\n'.join(map(str, o_by_date[int(c.data[:]):int(c.data[:]) + 5])) + '_',
                parse_mode='Markdown',
                reply_markup=pages_keyboard(int(c.data[:]), int(c.data[:]) + 5, m))
        else:
            pass
    except telebot.apihelper.ApiException:
        pass


general_information_past.close()
general_information_ongoing.close()
general_information_upcoming.close()

while True:
    try:
        bot.polling()
    except:
        time.sleep(5)
