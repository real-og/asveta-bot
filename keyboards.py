from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

subjects_kb_inline = InlineKeyboardMarkup()
math_i = InlineKeyboardButton('Математика', callback_data='Математика')
ru_i = InlineKeyboardButton('Русский', callback_data='Русский')
be_i = InlineKeyboardButton('Беларуская', callback_data='Беларуская')
en_i = InlineKeyboardButton('Английский', callback_data='Английский')
hi_i = InlineKeyboardButton('История', callback_data='История')
ph_i = InlineKeyboardButton('Физика', callback_data='Физика')
ch_i = InlineKeyboardButton('Химия', callback_data='Химия')
ge_i = InlineKeyboardButton('География', callback_data='География')
subjects_kb_inline.add(ru_i, be_i, en_i, hi_i, ph_i, ch_i, ge_i, )

class_kb_inline = InlineKeyboardMarkup()
c1_i = InlineKeyboardButton('1', callback_data='1')
c2_i = InlineKeyboardButton('2', callback_data='2')
c3_i = InlineKeyboardButton('3', callback_data='3')
c4_i = InlineKeyboardButton('4', callback_data='4')
c5_i = InlineKeyboardButton('5', callback_data='5')
c6_i = InlineKeyboardButton('6', callback_data='6')
c7_i = InlineKeyboardButton('7', callback_data='7')
c8_i = InlineKeyboardButton('8', callback_data='8')
c9_i = InlineKeyboardButton('9', callback_data='9')
c10_i = InlineKeyboardButton('10', callback_data='10')
c11_i = InlineKeyboardButton('11', callback_data='11')
class_kb_inline.add(c3_i, c4_i, c5_i, c6_i, c7_i, c8_i, c9_i, c10_i, c11_i)

time_kb_inline = InlineKeyboardMarkup()
morning_i = InlineKeyboardButton('08:30 - 13:00', callback_data='08:30 - 13:00')
mid_i = InlineKeyboardButton('13:00 - 18:00', callback_data='13:00 - 18:00')
evening_i = InlineKeyboardButton('18:00 - 22:00', callback_data='18:00 - 22:00')
time_kb_inline.add(morning_i, mid_i, evening_i)

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_kb.add('Изменить',
            'Поддержка',)

dialog_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('Окончить диалог')

# Создать билдеры клавиатур на основе листов из logic.py