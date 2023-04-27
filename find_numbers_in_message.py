from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import BaseFilter, Text, Command

BOT_TOKEN: str = '6140558942:AAEOFhwchO2_P3K8aGCB386dBbX0CQ28lJw'
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

# Этот фильтр будет проверять наличие неотрицательных чисел
# в сообщении от пользователя, и передавать в хэндлер их список
class NumbersInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        # Разрезаем сообщение по пробелам, нормализуем каждую часть, удаляя
        # лишние знаки препинания и невидимые символы, проверяем на то, что
        # в таких словах только цифры, приводим к целым числам
        # и добавляем их в список
        for word in message.text.split():
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        # Если в списке есть числа - возвращаем список по ключу 'numbers'
        if numbers:
            return {'numbers': numbers}
        return False


@dp.message(Command(commands=['start', 'help']))
async def start_command(message: Message):
    await message.answer(text='Привет! Я бот, находящий числа в твоём сообщении.\n'
                              'Напиши мне "найди числа" и я тебе их найду в твоём же сообщении.')


# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа" и в нем есть числа
@dp.message(Text(contains='найди числа', ignore_case=True), NumbersInMessage())
# Помимо объекта типа Message, принимаем в хэндлер список чисел из фильтра
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(text=f'Нашел: {", ".join(str(num) for num in numbers)}')


# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа", но в нем нет чисел
@dp.message(Text(contains='найди числа', ignore_case=True))
async def process_if_not_numbers(message: Message):
    await message.answer(text='Не нашел что-то :(')

if __name__ == '__main__':
    dp.run_polling(bot)