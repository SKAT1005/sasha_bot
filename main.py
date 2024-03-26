import os
import random
import threading
import time

import django
import telebot
from telebot import types

os.environ['DJANGO_SETTINGS_MODULE'] = 'sasha_bot.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from app.models import Memories, Congratulations

bot = telebot.TeleBot('7071542790:AAGLBF9X6V-PDSqcJAPXkfaHBvFR8haowu0')

congratulations_number = [1, len(Congratulations.objects.all()) + 1]
flag = [False]


def button():
    markup = types.InlineKeyboardMarkup()
    next = types.InlineKeyboardButton(text='Следующее поздравления', callback_data='next')
    markup.add(next)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id != 1:
        flag[0] = True
        congratulation = Congratulations.objects.get(id=congratulations_number[0])
        text = f'{congratulation.text}\n\n' \
               f'{congratulation.author}'
        if congratulations_number[0] + 1 != congratulations_number[1]:
            markup = button()
            if congratulation.photo:
                bot.send_photo(chat_id=chat_id, photo=congratulation.photo, caption=text, reply_markup=markup)
            else:
                bot.send_message(chat_id=chat_id, text=congratulation.text, reply_markup=markup)
        else:
            if congratulation.photo:
                bot.send_photo(chat_id=chat_id, photo=congratulation.photo, caption=text)
            else:
                bot.send_message(chat_id=chat_id, text=congratulation.text)


def send_congratulation(chat_id):
    if chat_id != 1:
        congratulation = Congratulations.objects.get(id=congratulations_number[0])
        text = f'{congratulation.text}\n\n' \
               f'{congratulation.author}'
        if congratulations_number[0] + 1 != congratulations_number[1]:
            markup = button()
            if congratulation.photo:
                bot.send_photo(chat_id=chat_id, photo=congratulation.photo, caption=text, reply_markup=markup)
            else:
                bot.send_message(chat_id=chat_id, text=congratulation.text, reply_markup=markup)
        else:
            flag[0] = True
            if congratulation.photo:
                bot.send_photo(chat_id=chat_id, photo=congratulation.photo, caption=text)
            else:
                bot.send_message(chat_id=chat_id, text=congratulation.text)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    if call.message:
        data = call.data
        if data == 'next':
            congratulations_number[0] += 1
            send_congratulation(chat_id=chat_id)


def send_memory():
    if flag[0]:
        for i in Memories.objects.all():
            try:
                if i.photo:
                    bot.send_photo(chat_id=1252306358, photo=i.photo, caption=i.text)
                else:
                    bot.send_message(chat_id=1252306358, text=i.text)
                time.sleep(60 * 60 * 24 * random.randint(1, 3))
            except Exception:
                pass
    time.sleep(60 * 60 * 10)


def polling_process():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    polling_thread = threading.Thread(target=polling_process)
    polling_thread.start()
    update_code = threading.Thread(target=send_memory)
    update_code.start()
