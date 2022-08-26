import telebot
import requests
import json
from random import randint


TOKEN = ''
bot = telebot.TeleBot(TOKEN)


def buscarConselhosCom(termo):
    requisicao = requests.get(f"https://api.adviceslip.com/advice/search/{termo}")
    texto = json.loads(requisicao.content)
    if 'slips' in texto.keys():
        conselho_aleatorio = randint(0, len(texto['slips']) - 1)
        return texto['slips'][conselho_aleatorio]['advice']
    else:
        return texto['message']['text']


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Type a word for an Advice: ')


@bot.message_handler(func=lambda m: True)
def text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    conselho = buscarConselhosCom(message.text)
    texto_final = f"Here's your advice for the word {message.text}: <b>{conselho}</b>"
    bot.reply_to(message, texto_final, parse_mode='html')


bot.polling()
