import telebot

bot = telebot.TeleBot("ТОКЕН_ТВОЕГО_БОТА")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! 👋")

bot.infinity_polling()
