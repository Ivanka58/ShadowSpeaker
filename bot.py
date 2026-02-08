import telebot
import pydub
import pydub.effects
import os
import tempfile
import pyttsx3

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
engine = pyttsx3.init()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот конвертирует текст в анонимный голос, просто отправь ему текст.')

@bot.message_handler(func=lambda message: True)
def convert_text_to_voice(message):
    text = message.text
    bot.send_chat_action(message.chat.id, action='record_audio')

    # Генерация обычного голоса с помощью pyttsx3
    engine.save_to_file(text, 'temp.mp3')
    engine.runAndWait()

    # Преобразование MP3 в объект AudioSegment
    sound = pydub.AudioSegment.from_mp3('temp.mp3')

    # Применение фильтрации (делаем голос ниже и приглушённее)
    modified_sound = sound.speedup(playback_speed=0.9)  # Замедление скорости воспроизведения
    modified_sound = modified_sound.low_pass_filter(100)  # Низкочастотный фильтр
    modified_sound.export('modified.mp3', format="mp3")  # Экспорт изменённого файла

    # Отправляем голос обратно пользователю
    with open('modified.mp3', 'rb') as audio_file:
        bot.send_audio(message.chat.id, audio_file)

    # Удаляем временные файлы
    os.remove('temp.mp3')
    os.remove('modified.mp3')

    bot.send_message(message.chat.id, 'Ваше сообщение готово! Спасибо за использование бота.')

if __name__ == "__main__":
    print("Starting the bot...")
    bot.polling(none_stop=True)
