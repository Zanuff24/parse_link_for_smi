import requests
import csv
import telebot
from telebot import types
import data
import datetime
import smi_list

bot = telebot.TeleBot(data.token) #https://t.me/parse_smi_bot

# dict. хранит запись вида id чата с сообщением, которое хранит последний отправленный текст от пользователя
# текст должен содержать ссылку + комментарий к ссылке
bd = {}

#запись в файл
# data дата отправки сообщения
# smi название сми
# link ссылка на пост
# comment  комментарий к ссылке
# chat id отправившего сообщение
def saveFile(chat, text, smi):
    with open('link_list.csv', "a", encoding='cp1251', newline='') as fill:
        data_now = datetime.datetime.now()
        link, comment = text.split()
        names = ["data", "smi", "link", " comment", "chat"]
        file_writer = csv.DictWriter(fill, delimiter=",",
                                     lineterminator="\r", fieldnames=names)
        file_writer.writerow({"data": data_now, "smi": smi, "link": link, " comment": comment, "chat": chat})


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "отправьте сообщение в формате: \n" +
                     "<b>ссылка комментарий </b>\n" +
                     "одна ссылка и комментарий за один раз", parse_mode='html')
#создание клавиатуры. список кнопок берется из записей smi_l файла smi_list

def keyboard():
    kb = types.InlineKeyboardMarkup()
    for el, name in smi_list.smi_l.items():
        kb.row(types.InlineKeyboardButton(text=name, callback_data=el))
    return kb

#прием сообщения в формате "ссылка + текст комментария"
@bot.message_handler(content_types=["text"])
def any_mes(message):
    if len(message.text.split()) != 2:
        bot.send_message(message.chat.id, "отправьте сообщение в формате: \n"+
                         "<b>ссылка комментарий </b>\n" +
                         "одна ссылка и комментарий за один раз", parse_mode='html')
    else:
        bd[message.chat.id] = message.text

        key = keyboard()
        bot.send_message(message.chat.id, "сми", reply_markup=key)

        print(message.chat.id, message.text)
        print(bd[message.chat.id])

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="сми")
    bot.send_message(call.message.chat.id, text=f'link{call.message.chat.id} + {bd[call.message.chat.id]}')
    saveFile(call.message.chat.id, bd[call.message.chat.id], smi_list.smi_l[call.data])

bot.polling(none_stop=True)