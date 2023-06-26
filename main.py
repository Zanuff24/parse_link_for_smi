import requests
import csv
import telebot
from telebot import types
import data
import datetime

bot = telebot.TeleBot(data.token) #https://t.me/parse_smi_bot
bd = {}

def saveFile(link, chat, smi):
    with open('link_list.csv', "a", encoding='cp1251', newline='') as fill:
        data_now = datetime.datetime.now()
        names = ["data", "smi", "link", "chat"]
        file_writer = csv.DictWriter(fill, delimiter=",",
                                     lineterminator="\r", fieldnames=names)
        file_writer.writerow({"data": data_now, "smi": smi, "link": link, "chat": chat})


def keyboard():
    kb = types.InlineKeyboardMarkup()
    sa = types.InlineKeyboardButton(text='Советская Адыгея', callback_data='sa')
    am = types.InlineKeyboardButton(text='Адыгэ макъ', callback_data='am')
    mn = types.InlineKeyboardButton(text='Майкопские новости', callback_data='mn')
    aif = types.InlineKeyboardButton(text='АИФ Адыгея', callback_data='aif')
    at = types.InlineKeyboardButton(text='Адыгея сегодня', callback_data='at')
    gtrk = types.InlineKeyboardButton(text='ГТРК', callback_data='gtrk')
    mtv = types.InlineKeyboardButton(text='МТВ', callback_data='mtv')
    sogl = types.InlineKeyboardButton(text='Согласие', callback_data='sogl')
    ed = types.InlineKeyboardButton(text='Единство', callback_data='ed')
    tv = types.InlineKeyboardButton(text='Теучежские вести', callback_data='tv')
    kz = types.InlineKeyboardButton(text='Красное знамя', callback_data='kz')
    mayak = types.InlineKeyboardButton(text='Маяк', callback_data='mayak')
    druz = types.InlineKeyboardButton(text='Дружба', callback_data='druz')
    zara = types.InlineKeyboardButton(text='Заря', callback_data='zara')
    kv = types.InlineKeyboardButton(text='Кошехабльские вести', callback_data='kv')
    ttv = types.InlineKeyboardButton(text='Тахтамукайское ТВ', callback_data='ttv')
    eic = types.InlineKeyboardButton(text='Единый информационный центр Шовгеновского района', callback_data='eic')

    kb.row(sa)
    kb.row(am)
    kb.row(mn)
    kb.row(aif)
    kb.row(at)
    kb.row(gtrk)
    kb.row(mtv)
    kb.row(sogl)
    kb.row(ed)
    kb.row(tv)
    kb.row(kz)
    kb.row(mayak)
    kb.row(druz)
    kb.row(zara)
    kb.row(kv)
    kb.row(ttv)
    kb.row(eic)
    return kb

@bot.message_handler(content_types=["text"])
def any_mes(message):
    bd.setdefault(message.chat.id, message.text)

    key = keyboard()
    bot.send_message(message.chat.id, "сми", reply_markup=key)

    print(message.chat.id, message.text)

    print(bd[message.chat.id])

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "sa":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="сми")
            bot.send_message(call.message.chat.id, text=f'link{call.message.chat.id} + {bd[call.message.chat.id]}')
            saveFile(call.message.chat.id, bd[call.message.chat.id], 'Советская Адыгея')

bot.polling(none_stop=True)