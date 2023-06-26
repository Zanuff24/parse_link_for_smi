import requests
import csv
import telebot
import data
import datetime

bot = telebot.TeleBot(data.token)

def saveFile(link, chat):
    with open('link_list.csv', "a", encoding='cp1251', newline='') as fill:
        data_now = datetime.datetime.now()
        names = ["data", "smi", "link", "chat"]
        file_writer = csv.DictWriter(fill, delimiter=",",
                                     lineterminator="\r", fieldnames=names)
        file_writer.writeheader()
        file_writer.writerow({"data": data_now, "smi": 'smi', "link": link, "chat": chat})


@bot.message_handler(content_types=["text"])
def any_mes(message):
    print(message.chat.id, message.text)
    saveFile(message.chat.id, message.text)


bot.polling(none_stop=True)