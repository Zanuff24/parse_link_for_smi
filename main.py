import csv
import telebot
from telebot import types
import datetime
import smi_list
import data

bot = telebot.TeleBot(data.token)

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
        first_whitespace = text.find(' ')
        link = text[:first_whitespace]
        comment = text[first_whitespace:]
        #link, comment = text.split()
        names = ["data", "smi", "link", " comment", "chat"]
        file_writer = csv.DictWriter(fill, delimiter=",",
                                     lineterminator="\r", fieldnames=names)
        file_writer.writerow({"data": data_now, "smi": smi, "link": link, " comment": comment, "chat": chat})


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "отправьте сообщение в формате: \n" +
                     "<b>ссылка комментарий </b>\n" +
                     "одна ссылка и комментарий за один раз", parse_mode='html')

@bot.message_handler(commands=['dfhfghfghfghfgh'])
def send(message):
    with open('link_list.csv', 'rb') as doc:
        bot.send_document(message.chat.id, doc,  parse_mode='html')

#создание клавиатуры. список кнопок берется из записей smi_l файла smi_list
def keyboard():
    kb = types.InlineKeyboardMarkup()
    for el, name in smi_list.smi_l.items():
        kb.row(types.InlineKeyboardButton(text=name, callback_data=el))
    return kb

#прием сообщения в формате "ссылка + текст комментария"
@bot.message_handler(content_types=["text"])
def any_mes(message):
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "отправьте сообщение в формате: \n" +
                         "<b>ссылка комментарий </b>\n" +
                        "пример \n" +
                        "https://aif.ru/ день независимости \n"
                         "одна ссылка и комментарий за один раз через пробел", parse_mode='html')
    else:
        bd[message.chat.id] = message.text

        key = keyboard()
        bot.send_message(message.chat.id, "сми", reply_markup=key)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="сми")
        bot.send_message(call.message.chat.id, text=f'данные сохранены')
        saveFile(call.message.chat.id, bd[call.message.chat.id], smi_list.smi_l[call.data])
    except:
        bot.send_message(call.message.chat.id, text=f'нет данных для сохранения. введите данные для отправки еще раз')
bot.polling(none_stop=True)