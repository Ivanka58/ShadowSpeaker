# bot.py
import telebot
from telebot import types
import os
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
    file_name = f"{message.chat.id}.mp3"
    
    # Конвертируем текст в голос
    engine.save_to_file(text, file_name)
    engine.runAndWait()
    
    with open(file_name, 'rb') as audio_file:
        bot.send_audio(message.chat.id, audio_file)
        
    bot.send_message(message.chat.id, 'Ваше сообщение готово! Спасибо за использование бота.')
    
    # Удаляем временный файл
    os.remove(file_name)

if __name__ == "__main__":
    print("Starting the bot...")
    bot.polling(none_stop=True)
