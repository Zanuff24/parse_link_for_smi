import requests
import csv
import telebot
import data

bot = telebot.TeleBot(data.token)

def saveFile(mas_url):
    with open('link_list.csv', "a", encoding='cp1251', newline='') as fill:
        writer = csv.writer(fill, delimiter=';')
        writer.writerow(mas_url)

if __name__ == '__main__':
    main()