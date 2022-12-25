from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
bot = Bot("5727777564:AAE8b-FTNSZ_uyO8J2X2FETJjQhEQkJVMB4")
dp = Dispatcher(bot)
ua = UserAgent()

@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.chat.id, f"""
Привет! <b> {message.from_user.first_name} </b>Я бот, который позволит быстро находить нужные товары в <b><a href="https://www.21vek.by">21 vek</a></b>

Для того, чтобы я отправил тебе товар, введи в поле его название...""",
                           parse_mode="html", disable_web_page_preview=1)


@dp.message_handler(content_types=['text'])
async def parser(message: types.message):
    url = "https://www.21vek.by/search/?sa=&term=_" + message.text
    print(url)
    request = requests.get(
        url,
        headers={'user-agent': f'{ua.random}'}
    )
    soup = BeautifulSoup(request.text, "html.parser")

    all_links = soup.find_all("a", class_="result__link j-ga_track")
    print(len(all_links))
    for link in all_links:
        print(link['href'])
        url = "" + link["href"]
        request = requests.get(
            url,
            headers={'user-agent': f'{ua.random}'}
        )
        soup = BeautifulSoup(request.text, "html.parser")

        name = soup.find("div", class_="content__header").find('h1').text
        price = soup.find("div", class_="item-price").find('span').text

        await bot.send_message(message.chat.id,
                               "<b>" + name + "</b>\n<i>" + price + f"</i>\n<a href='{url}'>Ссылка на сайт</a>",
                               parse_mode="html", disable_web_page_preview=1)
        if all_links.index(link) == 9:
            break

        if len(all_links) == 0:
            await bot.send_message(message.chat.id, "Ничего не найдено")

executor.start_polling(dp)
