import telebot
import requests
from bs4 import BeautifulSoup
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
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def give_fact(message, curr=["nils-bor-i-dom-s-truboj-s-pivom/"]):
    address = "https://zagge.ru/"

    r = requests.get(address + curr[0])
    soup = BeautifulSoup(r.text, 'html.parser')
    for info in soup.select('#main'):
        nxt = info.select('.more-facts')[0]
        curr[0] = nxt.get('href')

    for info in soup.select('#main'):
        fact = info.select('.af-description')[0].text
        fact = fact.split("Больше фактов")[0]
        image = info.select('.af-image-ratio')[0].img
        src = image.get('src')

    bot.send_message(message.from_user.id, text=fact)
    bot.send_photo(message.from_user.id, src)


bot.polling(none_stop=True, interval=0)
