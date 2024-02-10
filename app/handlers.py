from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from filters import InstanceFilter
from curparser import Currency

router = Router()
currency = Currency()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer('''Привет, это бот для отслеживания курса валют. Мои команды:\n
/rates = вывести курсы валют
/prices [кол-во] - цена кол-ва каждой валюты в рублях
/rub [кол-во] - цена кол-ва рублей в каждой валюте
/upd - обновить курсы валют''')

@router.message(Command('rates'))
async def r_handler(msg: Message):
    rates = currency.get()
    ratestext = ''
    for rate in currency.get():
        ratestext += f'1 {rate.upper()} = {rates[rate]} RUB\n'
    await msg.reply(f'Текущий курс валют:\n{ratestext}')

@router.message(Command('prices'), InstanceFilter(int))
async def pr_handler(msg: Message):
    qty = msg.text.split()[1]
    rates = currency.get()
    ratestext = ''
    for rate in currency.get():
        ratestext += f'{qty} {rate.upper()} = {rates[rate]*int(qty)} RUB\n'
    await msg.reply(f'Курс валют в кол-ве {qty}:\n{ratestext}')

@router.message(Command('prices'))
async def badpr_handler(msg: Message):
    await msg.reply('Неверный синтаксис! Пиши: /prices [кол-во]')

@router.message(Command('rub'), InstanceFilter(int))
async def rub_handler(msg: Message):
    qty = msg.text.split()[1]
    rates = currency.get()
    ratestext = ''
    for rate in currency.get():
        ratestext += f'{round(int(qty)/rates[rate],2)} {rate.upper()} = {qty} RUB\n'
    await msg.reply(f'Курс рубля в кол-ве {qty}:\n{ratestext}')

@router.message(Command('rub'))
async def badrub_handler(msg: Message):
    await msg.reply('Неверный синтаксис! Пиши: /rub [кол-во]')

@router.message(Command('upd'))
async def upd_handler(msg: Message):
    await currency.update()
    await msg.reply('Курсы валют обновлены!')

@router.message(F.text[0] == '/')
async def upd_handler(msg: Message):
    await msg.reply('Неизвестная команда! Напишите /start чтобы узнать список команд')