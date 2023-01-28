from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
import os
import logging
from keyboards import *
from logic import WorkSheet
from logic import time_periods, subjects, classes, admin_ids

logging.basicConfig(level=logging.INFO)

API_TOKEN = str(os.environ.get('BOT_TOKEN'))

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class State(StatesGroup):
    choose_subject = State()
    choose_class = State()
    choose_time = State()
    choose_email = State()
    menu = State()
    text_support = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("""<b>Привет-привет!</b>\nЗдесь ты можешь оставить заявку на онлайн-уроки для закрепления школьной программы <a href="https://asveta.by/">Asveta.by</a>.\n\nВыбирай <b>Предмет</b>, нажимая на кнопку""", parse_mode='HTML', reply_markup=subjects_kb_inline)
    await State.choose_subject.set()

@dp.callback_query_handler(state=State.choose_subject, text=subjects)
async def set_subject(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_subject=callback.data)
    await callback.message.answer("Теперь давай определимся с <b>классом</b>", reply_markup=class_kb_inline, parse_mode='HTML')
    await State.choose_class.set()
    await bot.answer_callback_query(callback.id)
    
@dp.callback_query_handler(state=State.choose_class, text=classes)
async def set_class(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_class=callback.data)
    await callback.message.answer("Выбирай удобное <b>время</b>", reply_markup=time_kb_inline, parse_mode='HTML')
    await State.choose_time.set()
    await bot.answer_callback_query(callback.id)

@dp.callback_query_handler(state=State.choose_time, text=time_periods)
async def set_time(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_time=callback.data)
    await callback.message.answer("Оставь свой <b>email или номер телефона</b> на всякий случай", parse_mode='HTML')
    await State.choose_email.set()
    await bot.answer_callback_query(callback.id)

@dp.message_handler(state=State.choose_email)
async def set_email(message: types.Message, state: FSMContext):
    await State.menu.set()
    user_data = await state.get_data()
    await message.answer("Твоя заявка принята!\n\n<i>Ты можешь изменить её, а если возникли вопросы - написать в поддержку.</i>", parse_mode='HTML', reply_markup=menu_kb)
    WorkSheet().append_request(user_data['chosen_subject'],
                                user_data['chosen_class'],
                                user_data['chosen_time'],
                                message.text.lower(),)
    
@dp.message_handler(state=State.menu, text='Изменить')
async def add_request(message: types.Message, state: FSMContext):
    await message.answer("Окей, заполняем форму ещё раз\nВыбирай <b>Предмет</b>", parse_mode='HTML', reply_markup=subjects_kb_inline)
    await State.choose_subject.set()

@dp.message_handler(state=State.menu, text='Поддержка')
async def text_support(message: types.Message, state: FSMContext):
    await message.answer("Пиши, с чем возникли трудности. Ответ придёт прямо сюда.\n\nИмей в виду, что в настройках приватности должно стоять <b>разрешение</b> на просмотр профиля в пересланных сообщениях", parse_mode='HTML')
    await State.text_support.set()

@dp.message_handler(state=State.text_support, text="Окончить диалог")
async def text_support(message: types.Message, state: FSMContext):
    await State.menu.set()
    await message.answer('Вы вернулись', parse_mode='HTML', reply_markup=menu_kb)    

@dp.message_handler(state=State.text_support)
async def text_support(message: types.Message, state: FSMContext):
    await message.answer("Принято", parse_mode='HTML', reply_markup=dialog_kb)
    for admin_id in admin_ids:
        await bot.forward_message(chat_id=admin_id, from_chat_id=message.from_id, message_id=message.message_id)

@dp.message_handler(filters.IDFilter(chat_id=admin_ids), state='*')
async def choose_cos(message: types.Message):
    if message.reply_to_message == None:
        await message.answer(f"Вы админ. Используйте <b>ответить</b>", parse_mode='HTML')
    elif message.reply_to_message.forward_from == None:
        await message.answer(f"Аккаунт закрыт", parse_mode='HTML')
    else:
        who = message.reply_to_message.forward_from.id
        await bot.send_message(chat_id=who, text=message.text, reply_markup=dialog_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)