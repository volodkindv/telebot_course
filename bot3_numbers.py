import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Text, BaseFilter
from aiogram.types import Message

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
API_TOKEN: str = os.getenv("BOT_TOKEN")

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
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

# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа" и в нем есть числа
@dp.message(Text(startswith='найди числа', ignore_case=True),
            NumbersInMessage())
# Помимо объекта типа Message, принимаем в хэндлер список чисел из фильтра
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(
            text=f'Нашел: {str(", ".join(str(num) for num in numbers))}')


# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа", но в нем нет чисел
@dp.message(Text(startswith='найди числа', ignore_case=True))
async def process_if_not_numbers(message: Message):
    await message.answer(
            text='Не нашел что-то :(')


if __name__ == "__main__":
    dp.run_polling(bot)
