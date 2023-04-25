import random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command

BOT_TOKEN: str = '6140558942:AAEOFhwchO2_P3K8aGCB386dBbX0CQ28lJw'
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

ATTEMPTS: int = 7

user: dict = {'in_game': False,
              'random_number': None,
              'attempts': None,
              'total_games': 0,
              'wins': 0}
def get_random_number() -> int:
    return random.randint(1, 100)

@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer(f'Всего игр сыграно: {user["total_games"]}\nИгр выиграно: {user["wins"]}')

@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')

@dp.message(Command(commands=['cancel']))
async def cancel_command(message: Message):
    if user['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть снова - напишите об этом')
        user['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. Может, сыграем разок?')

# ignore_case означает игнорирование регистра
# т.е. через фильтр пройдут сообщения "Да", "ДА", "да", "дА", "ДаВаЙ" и т.д.
@dp.message(Text(text=['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть'], ignore_case=True))
async def positive_answer(message: Message):
    if user['in_game']:
        await message.answer('Пока мы играем в игру я могу реагировать только '
                             'на числа от 1 до 100 и команды /cancel и /stat')
    else:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, попробуй угадать!')
        user['in_game'] = True
        user['random_number'] = get_random_number()
        user['attempts'] = ATTEMPTS

@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def negative_answer(message: Message):
    if user['in_game']:
        await message.answer('Пока мы играем в игру я могу реагировать только '
                             'на числа от 1 до 100 и команды /cancel и /stat')
    else:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')

@dp.message(lambda x: x.text and x.text.isdigit() and 1<=int(x.text)<=100)
async def number_answer(message: Message):
    if user['in_game']:
        if user['attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось попыток. Вы проиграли :(\n\nМое число '
                                 f'было {user["random_number"]}\n\nДавайте сыграем еще?')
        if int(message.text) == user['random_number']:
            await message.answer('Ура!!! Вы угадали число!\n\nМожет, сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
        elif int(message.text) < user['random_number']:
            user['attempts'] -= 1
            await message.answer('Мое число больше')
        elif int(message.text) > user['random_number']:
            user['attempts'] -= 1
            await message.answer('Мое число меньше')
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')

@dp.message()
async def other_text_message(message: Message):
    if user['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')

if __name__ == '__main__':
    dp.run_polling(bot)