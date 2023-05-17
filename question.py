from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import (ReplyKeyboardMarkup, Message, KeyboardButton,
                           ReplyKeyboardRemove)

API_TOKEN: str = '6140558942:AAEOFhwchO2_P3K8aGCB386dBbX0CQ28lJw'

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Создаём объекты кнопок
button1: KeyboardButton = KeyboardButton(text='Собак 🦮')
button2: KeyboardButton = KeyboardButton(text='Огурцов 🥒')

# Создаём объект клавиатуры и крепим на него кнопки
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button1, button2]],
                                                    resize_keyboard=True)

@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text='Чего кошки боятся больше?',
                         reply_markup=keyboard)

@dp.message(Text(text='Собак 🦮'))
async def answer_dog(message:Message):
    await message.answer(text='Да, несомненно, кошки боятся собак. '
                              'Но вы видели как они боятся огурцов?',
                         reply_markup=ReplyKeyboardRemove())

@dp.message(Text(text='Огурцов 🥒'))
async def answer_cucumber(message: Message):
    await message.answer(text='Да, иногда кажется, что огурцов '
                              'кошки боятся больше',
                         reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    dp.run_polling(bot)