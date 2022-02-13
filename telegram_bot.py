# Simple Telegram Bot
from cmath import nan
import subprocess
import os
import pandas as pd
import telebot
from telebot import types

bot = telebot.TeleBot('')
@bot.message_handler(commands=["start"])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("Rekognition")
    item2 = types.KeyboardButton("Get results")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id, 'Send picture as file', reply_markup=markup)
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Rekognition' :
        dir = os.listdir('/data/')
        if len(dir) == 0:
            bot.send_message(message.chat.id, 'Error! First you must send picture')
        else:
            subprocess.Popen(['python3', 'amazon_rekognition.py'])
            bot.send_message(message.chat.id, 'Done! Press Get results button to continue...')
    elif message.text.strip() == 'Get results':
        data = pd.read_csv('/results/awsrekognition_celeb_detect.csv')
        celeb_full_name = str(data.at[0, 'celeb_name'])
        if celeb_full_name == str(nan):
            bot.send_message(message.chat.id, 'Celebrity not found!')
        else:
            if celeb_full_name != str(nan):
                bot.send_message(message.chat.id, 'On picture' + celeb_full_name)
                celeb_match_conf = str(data.at[0, 'celeb_match_conf'])
                bot.send_message(message.chat.id, 'Match percent: ' + celeb_match_conf + '%')
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = '/data/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            bot.reply_to(message, "Upload successul!")
    except Exception as e:
        bot.reply_to(message, e)
bot.polling(none_stop=True, interval=0)