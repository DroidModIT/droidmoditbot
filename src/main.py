import telebot

import config

bot = telebot.TeleBot(config.BOT_TOKEN, skip_pending=True, num_threads=config.THREADS)

if __name__ == '__main__':
    bot.polling(none_stop=True)
