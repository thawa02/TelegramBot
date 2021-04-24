import telebot
import requests
from bs4 import BeautifulSoup as BS
import urllib
import tkn  #тут лежал токен


bot = telebot.TeleBot(tkn.token)


@bot.message_handler(commands=['start'])
def send(message):
    to_send = "Добро пожаловать! Я знаю много интересных фактов и хочу ими поделиться! Чтобы получить факт, пиши /fact"
    bot.send_message(message.from_user.id, text=to_send)


@bot.message_handler(commands=['help'])
def send(message):
    bot.send_message(message.from_user.id, text="Чтобы получить факт, пиши /fact")


@bot.message_handler(commands=['fact'])
def send(message):
    give_fact(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Привет!")
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        bot.send_message(message.from_user.id, text='Хочешь интересный факт?', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        give_fact(call.message)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Ну как знаешь")


def give_fact(message, curr=["nils-bor-i-dom-s-truboj-s-pivom/"]):
    address = "https://zagge.ru/"
    page = urllib.request.urlopen(address + curr[0]).read()
    lst = page.split()
    nxt = lst[lst.index(b'\xd0\xa4\xd0\x90\xd0\x9a\xd0\xa2\xd0\x9e\xd0\x92!</a>') - 1].decode()
    curr[0] = nxt.split('"')[1]

    r = requests.get(address + curr[0])
    html = BS(r.content, 'html.parser')
    for info in html.select('#main'):
        fact = info.select('.af-description')[0].text
        fact = fact.split("Больше фактов")[0]

    bot.send_message(message.from_user.id, text=fact)


bot.polling(none_stop=True, interval=0)
