from telebot import types

import telebot
import time

token = '520114385:AAHPgTD1iqSNnZ3u0m4lcUsfBf6Wi1BC-ZM'

bot = telebot.TeleBot("520114385:AAHPgTD1iqSNnZ3u0m4lcUsfBf6Wi1BC-ZM")

general_information_ongoing = open("general_information_ongoing.txt", 'r')
info = general_information_ongoing.readlines()

def pages_keyboard(start, stop):
    keyboard = types.InlineKeyboardMarkup()
    btns = []
    if start > 0: btns.append(types.InlineKeyboardButton(
        text='⬅', callback_data='to_{}'.format(start - 10)))
    if stop < len(info): btns.append(types.InlineKeyboardButton(
        text='➡', callback_data='to_{}'.format(stop)))
    keyboard.add(*btns)
    return keyboard

@bot.message_handler(commands=['start'])
# handle start message
def start(m):
    bot.send_message(
        m.chat.id,
        '_' + '\n'.join(map(str, info[:10])) + '_',
        parse_mode='Markdown',
        reply_markup=pages_keyboard(0, 10))

@bot.callback_query_handler(func=lambda c: c.data)
def pages(c):
    try:
        time.sleep(2) #avoid many requests per second
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text = '_' + '\n'.join(map(str, info[int(c.data[3:]):int(c.data[3:]) + 10])) + '_',
            parse_mode='Markdown',
            reply_markup=pages_keyboard(int(c.data[3:]),
                int(c.data[3:]) + 10))
    except telebot.apihelper.ApiException as e:
        print(str(e))
        time.sleep(5)



general_information_ongoing.close()

while True:
    try:
        bot.polling()
    except:
        time.sleep(5)