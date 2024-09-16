from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

API_KEY = ''
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()


button_man = KeyboardButton('Мужчина')
button_woman = KeyboardButton('Девушка')
button_calories = KeyboardButton('Рассчитать Калории')
button_info = KeyboardButton('Информация')
sex_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_man).add(button_woman)
start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_calories).add(button_info)


@dp.message_handler(commands=['start'])
async def start(message):
    print(message.text)
    print('Привет! Я Бот помогающий твоему здоровью')
    await message.answer('Привет! Я помогаю тебе с учетом питания и здоровья', reply_markup=start_kb)

@dp.message_handler(text='Информация')
async def info(message: types.Message):
    await message.answer('Бот создан для помощи в учете питания и здоровья')
    await message.answer('Пока что вы можете рассчитать калории')

@dp.message_handler(text='Рассчитать Калории')
async def set_sex(message: types.Message):
    print(message.text)
    await message.answer('Введите ваш пол м/ж', reply_markup=sex_kb)
    await UserState.sex.set()


@dp.message_handler(state=UserState.sex)
async def set_age(message, state):
    print(message.text)
    await state.update_data(sex_=message.text)
    await message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    print(message.text)
    await state.update_data(age_=message.text)
    await message.answer('Введите свой рост в сантиметрах')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    print(message.text)
    await state.update_data(growth_=message.text)
    await message.answer('Введите свой вес в килограммах')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    print(message.text)
    await state.update_data(weight_=message.text)
    data = await state.get_data()
    data['growth'] = int(data.pop('growth_'))  # Convert 'growth' to integer
    data['weight'] = int(data.pop('weight_'))  # Convert 'weight' to integer
    data['age'] = int(data.pop('age_'))  # Convert 'age' to integer
    data['sex'] = data.pop('sex_')  # Update 'sex' key
    if data['sex'] == 'Мужчина':
        calories_result = 10 * data['growth'] + 6.25 * data['weight'] - 5 * data['age'] + 5
        await message.answer(f'Ваш результат в калориях: {calories_result}')
    elif data['sex'] == 'Девушка':
        calories_result = 10 * data['growth'] + 6.25 * data['weight'] - 5 * data['age'] - 161
        await message.answer(f'Ваша норма в калориях: {calories_result}')
    print(calories_result)
    await state.finish()


@dp.message_handler()
async def all_mess(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

