import telebot
from telebot import types
import requests
import random


from bs4 import BeautifulSoup as bs


def get_weather(city_name):
    pass
    city_dict = {
        'москва': 'moskva',
        'казань': 'kazan',
        'сочи': 'sochi',
        'люберцы': 'lyubertsyi'
    }
    city = city_dict[city_name.lower()]

    url = f'https://www.meteoservice.ru/weather/overview/{city}'

    proxies = (
        {"http": "socks5://72.206.181.97:64943"},
        {"http": "157.245.33.179:80"},
        {"http": "161.35.78.6:80"},
        {"https": "43.134.211.251:1080"}
    )

    proxy = random.choice(proxies)

    print(proxy)

    response = requests.get(url=url, proxies=proxy)
    soup = bs(response.text, 'lxml')

    temp = soup.find('span', class_="value")

    description = soup.find(
        class_='text-description'
    ).text.strip()

    description_string = [
        f'{elem.strip()}' for elem in description.split('. ')
    ]

    res = ''
    for elem in description_string:
        res += ''.join(f'{elem}\n')

    return f'Температура сейчас: {temp.text}\nОщущается как: {temp.text}\n' \
           f'{res}'


bot = telebot.TeleBot('API_KEY')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button_1 = types.KeyboardButton('Москва')
    button_2 = types.KeyboardButton('Люберцы')
    button_3 = types.KeyboardButton('Казань')
    button_4 = types.KeyboardButton('Сочи')
    markup.add(button_1, button_2, button_3, button_4)
    bot.send_message(message.chat.id, "Choose the city: ", reply_markup=markup)


@bot.message_handler(content_types='text')
def send_weather(message):
    if message.text in ['Москва', 'Люберцы', 'Казань', 'Сочи']:
        bot.send_message(message.chat.id, get_weather(message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)