import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import redis

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Настройка Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я ваш бот. Отправьте мне любое сообщение, и я сохраню его в Redis.')

# Функция для обработки текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    # Сохранение сообщения в Redis
    redis_client.rpush('messages', user_message)
    await update.message.reply_text(f'Сообщение сохранено: {user_message}')

def main():
    # Вставьте ваш токен сюда
    app = ApplicationBuilder().token("7868797759:AAFUiuJNpCZ9pEQ0xS1GXKM_nKJ8J7wligc").build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    app.run_polling()

if __name__ == '__main__':
    main()
