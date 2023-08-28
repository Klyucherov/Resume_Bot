from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='/help')
b2 = KeyboardButton(text='/About')
b3 = KeyboardButton(text='Мои фото')

kb.add(b1, b2).add(b3)

kb_photo = ReplyKeyboardMarkup(resize_keyboard=True)
bp1 = KeyboardButton(text='Рандом')
bp2 = KeyboardButton(text='Главное меню')

kb_photo.add(bp1, bp2)

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='❤️',
                           callback_data='like')
ib2 = InlineKeyboardButton(text='👎',
                           callback_data='dislike')
ib3 = InlineKeyboardButton(text='Следующая фотка',
                           callback_data='next_photo')  # Обратите внимание на название коллбека
ib4 = InlineKeyboardButton(text='Главное меню',
                           callback_data='main')

ikb.add(ib1, ib2).add(ib3).add(ib4)

answers_button = KeyboardButton(text='Ответы на вопросы')
github_button = KeyboardButton(text='Дай мне ссылку')

kb.add(answers_button)

audio_kb = InlineKeyboardMarkup(row_width=1)

gpt_button = InlineKeyboardButton(text="Что такое GPT", callback_data="gpt_explanation")
sql_button = InlineKeyboardButton(text="Разница между SQL и NoSQL", callback_data="sql_nosql_difference")
love_button = InlineKeyboardButton(text="История первой любви", callback_data="first_love_story")

audio_kb.add(gpt_button, sql_button, love_button)
