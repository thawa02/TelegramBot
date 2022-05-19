import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import tkn
import tests


bot = telebot.TeleBot(tkn.token)
start_address = "nils-bor-i-dom-s-truboj-s-pivom/"
site_address = "https://zagge.ru/"


@bot.message_handler(commands=['start'])
def send(message):
    to_send = "Добро пожаловать! Я знаю много интересных фактов и хочу ими поделиться! " \
              "Чтобы получить факт, пиши /fact или нажми на кнопку"

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text="Получить факт")
    keyboard.add(button)

    bot.send_message(message.from_user.id, text=to_send, reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send(message):
    bot.send_message(message.from_user.id, text="Чтобы получить факт, пиши /fact или нажми на кнопку")


@bot.message_handler(commands=['fact'])
def send(message):
    send_fact(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Получить факт":
        send_fact(message)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def send_fact(message, curr=[start_address]):
    """Оправляет пользователю факт и картинку"""

    r = requests.get(site_address + curr[0])
    soup = BeautifulSoup(r.text, 'html.parser')

    fact = get_fact(soup)

    bot.send_message(message.from_user.id, text=fact[0])
    bot.send_photo(message.from_user.id, fact[1])

    curr[0] = get_next_page(soup)


def get_fact(soup):
    """Возвращает текст факта и ссылку на картинку"""

    for info in soup.select('#main'):
        fact = info.select('.af-description')[0].text
        fact = fact.split("Больше фактов")[0]
        fact = fact.split("Подробнее")[0]
        image = info.select('.af-image-ratio')[0].img
        src = image.get('src')

    return [fact, src]


def get_next_page(soup):
    """Возвращает ссылку на страницу со следующим фактом"""

    for info in soup.select('#main'):
        nxt = info.select('.more-facts')[0]
        return nxt.get('href')


bot.polling(none_stop=True, interval=0)
