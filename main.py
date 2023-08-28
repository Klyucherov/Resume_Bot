import os

import dotenv
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from aiogram.types import ReplyKeyboardRemove

from keyboards import kb, ikb, audio_kb

dotenv.load_dotenv()

# Установите ваш API-ключ OpenAI
bot_key = os.getenv('BOT_TOKEN')
open_key = os.getenv('OPEN_API')

openai.api_key = open_key
bot = Bot(token=bot_key)  # создаём экземпляр бота, подключаясь к API
dp = Dispatcher(bot=bot)

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>запуск бота</em>
<b>/About</b> - <em>Обо мне</em>"""

INFO = """
Ключеров Евгений, 23 года

Моё главное увлечение это программирование, на него я трачу больше всего времени.

С утра я занимаюсь учебными и пет проектами. Читаю теорию, пишу код. В среднем трачу на это  по 2-4 часа день.

После обеда занимаюсь рабочими задачами, так же пишу код, добавляю новый функционал на сайт или рефакторю код.

Вечером с 18.00 до 22.00 я преподаю программирование детям 9 - 16 лет.
"""

current_photo_index = 0
flag = False

photo_folder = "photo"
photo_files = os.listdir(photo_folder)


async def on_startup(_):
    print('Я запустился!')


@dp.message_handler(content_types=[types.ContentType.VOICE])
async def handle_voice_message(message: types.Message):
    audio = await bot.download_file_by_id(message.voice.file_id)

    try:
        response = openai.SpeechToText.create(audio=audio)
        text = response['text']

        if "Дай мне ссылку" in text:
            await message.answer("Конечно! Вот ссылка на мой GitHub: https://github.com/Klyucherov")
        else:
            await message.answer("Вы сказали: " + text)
    except Exception as e:
        await message.answer("Произошла ошибка при распознавании речи." + str(e))


async def send_current_photo(message: types.Message):
    if 0 <= current_photo_index < len(photo_files):
        photo_path = os.path.join(photo_folder, photo_files[current_photo_index])
        photo_name = os.path.splitext(photo_files[current_photo_index])[0]
        await bot.send_photo(chat_id=message.chat.id,
                             photo=open(photo_path, 'rb'),
                             caption=photo_name,
                             reply_markup=ikb)


@dp.message_handler(Text(equals="Мои фото"))
async def show_my_photos(message: types.Message):
    global current_photo_index
    await message.answer(text='Ваши фотографии по порядку!',
                         reply_markup=ReplyKeyboardRemove())
    await send_current_photo(message)
    await message.delete()


@dp.message_handler(Text(equals="Ответы на вопросы"))
async def show_answers_menu(message: types.Message):
    await message.answer(text='Выберите вопрос:',
                         reply_markup=audio_kb)
    await message.delete()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text='Добро пожаловать в наш бот! 🐝',
                         reply_markup=kb)
    await message.delete()


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer(text=HELP_COMMAND,
                         parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['About'])
async def cmd_help(message: types.Message):
    await message.answer(text=INFO)
    await bot.send_sticker(chat_id=message.chat.id,
                           sticker="CAACAgIAAxkBAAEKGUBk5bZEsDlxEdKvUXHF2p_ftRjwSgACOR8AAuMNwUiX2rsmPHIbxTAE")
    await message.delete()


# Добавим обработку кнопок лайка и дизлайка
@dp.callback_query_handler(Text(equals='like'))
async def callback_like(callback: types.CallbackQuery):
    await callback.answer("Вам понравилось!")


@dp.callback_query_handler(Text(equals='dislike'))
async def callback_dislike(callback: types.CallbackQuery):
    await callback.answer("Вам не понравилось!")


# Обработка коллбека кнопки "Главное меню"
@dp.callback_query_handler(Text(equals='main'))
async def callback_main(callback: types.CallbackQuery):
    await callback.message.answer(text='Добро пожаловать в главное меню!',
                                  reply_markup=kb)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(Text(equals='next_photo'))  # Обработка коллбека только для "Следующая фотка"
async def callback_next_photo(callback: types.CallbackQuery):
    global current_photo_index
    current_photo_index = (current_photo_index + 1) % len(photo_files)
    photo_path = os.path.join(photo_folder, photo_files[current_photo_index])

    photo_name = os.path.splitext(photo_files[current_photo_index])[0]  # Получаем имя файла без расширения
    await callback.message.edit_media(types.InputMedia(media=types.InputFile(photo_path),
                                                       type='photo',
                                                       caption=photo_name),
                                      # Используем имя файла без расширения в качестве описания
                                      reply_markup=ikb)
    await callback.answer()


@dp.callback_query_handler(Text(equals='gpt_explanation'))
async def callback_gpt_explanation(callback: types.CallbackQuery):
    audio_path = "audio/gpt_explanation.ogg"
    await bot.send_voice(callback.message.chat.id, voice=InputFile(audio_path))


@dp.callback_query_handler(Text(equals='sql_nosql_difference'))
async def callback_sql_nosql_difference(callback: types.CallbackQuery):
    audio_path = "audio/sql_nosql_difference.ogg"
    await bot.send_voice(callback.message.chat.id, voice=InputFile(audio_path))


@dp.callback_query_handler(Text(equals='first_love_story'))
async def callback_first_love_story(callback: types.CallbackQuery):
    audio_path = "audio/first_love_story.ogg"
    await bot.send_voice(callback.message.chat.id, voice=InputFile(audio_path))


@dp.message_handler(Text(equals="Дай мне ссылку"))
async def send_github_link(message: types.Message):
    await message.answer("Конечно! Вот ссылка на мой GitHub: https://github.com/Klyucherov")


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
