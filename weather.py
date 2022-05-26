import telebot
from telebot import types
import requests
from fake_useragent import UserAgent


from bs4 import BeautifulSoup as bs


def get_weather(city_name):
    city_dict = {
        'москва': 'moskva',
        'казань': 'kazan',
        'сочи': 'sochi',
        'люберцы': 'lyubertsyi'
    }
    city = city_dict[city_name.lower()]

    url = f'https://www.meteoservice.ru/weather/overview/{city}'

    ua = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    user_city_id = {'moskva': '1',
                    'sochi': '18253',
                    'kazan': '139',
                    'lyubertsyi': '142'}

    cookies = {
        'user_city_id': user_city_id[city],
    }

    response = requests.get(url=url, headers=headers, cookies=cookies)
    soup = bs(response.text, 'lxml')

    temp = soup.find('span', class_="value")

    description = soup.find(
        class_='text-description'
    ).text.strip()

    description_string = [
        f'{elem.strip()}' for elem in description.split(',')
    ]

    res = ''
    for elem in description_string:
        res += ''.join(f'{elem.strip()}\n')

    return f'Температура сейчас: {temp.text}\nОщущается как: {temp.text}\n{res}'


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
        print(message.text)
        bot.send_message(message.chat.id, get_weather(message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
