import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from src.runner import AppRunner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
runner = AppRunner()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для сбора и обработки новостей.\n"
        "Команды:\n"
        "/collect – запустить сбор данных\n"
        "/sources – настроить источники\n"
        "/strategy – выбрать стратегию обработки\n"
        "/mode – выбрать режим выполнения\n"
        "/stats – показать результат последнего запуска"
    )

async def collect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Начинаю сбор данных...")
    try:
        result = await runner.run()
        if len(result) > 4000:
            result = result[:4000] + "...\n(результат обрезан)"
        await update.message.reply_text(f"Результат:\n{result}")
    except Exception as e:
        logger.exception("Ошибка при сборе данных")
        await update.message.reply_text(f"Произошла ошибка: {e}")

async def sources_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Демо", callback_data="src_demo")],
        [InlineKeyboardButton("Файл", callback_data="src_file")],
        [InlineKeyboardButton("Веб", callback_data="src_web")],
        [InlineKeyboardButton("Все сразу", callback_data="src_all")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите источники:", reply_markup=reply_markup)

async def strategy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Нормализация", callback_data="strategy_normalization")],
        [InlineKeyboardButton("Фильтрация", callback_data="strategy_filter")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите стратегию:", reply_markup=reply_markup)

async def mode_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Последовательный", callback_data="mode_sequential")],
        [InlineKeyboardButton("Потоки", callback_data="mode_threads")],
        [InlineKeyboardButton("Процессы", callback_data="mode_processes")],
        [InlineKeyboardButton("Асинхронный", callback_data="mode_async")],
        [InlineKeyboardButton("Гибридный", callback_data="mode_hybrid")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите режим выполнения:", reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if runner.last_result:
        await update.message.reply_text(f"Последний результат:\n{runner.last_result[:4000]}")
    else:
        await update.message.reply_text("Ещё не было запусков.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("src_"):
        context.user_data['sources'] = data
        await query.edit_message_text(f"Выбран источник: {data}")
    elif data.startswith("strategy_"):
        strategy = data.replace("strategy_", "")
        runner.config.strategy_name = strategy
        await query.edit_message_text(f"Выбрана стратегия: {strategy}")
    elif data.startswith("mode_"):
        mode = data.replace("mode_", "")
        runner.config.mode = mode
        await query.edit_message_text(f"Выбран режим: {mode}")
    else:
        await query.edit_message_text("Неизвестная команда")

def main():
    import os
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Не задан TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("collect", collect))
    application.add_handler(CommandHandler("sources", sources_menu))
    application.add_handler(CommandHandler("strategy", strategy_menu))
    application.add_handler(CommandHandler("mode", mode_menu))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
