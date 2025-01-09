import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توکن‌های شما
TELEGRAM_TOKEN = "8153522655:AAHwdHy93cdYbUGOORD05sElI19Ps6IX86w"
OPENAI_API_KEY = "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"

# تنظیم OpenAI
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من بات تلگرام متصل به OpenAI هستم. دستورات موجود:\n"
        "/start - شروع بات\n"
        "/help - راهنما\n"
        "پیامت رو بفرست تا جوابت رو بدم!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سوالی داری؟ بپرس!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        # درخواست به OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=150
        )

        # پاسخ به کاربر
        bot_response = response['choices'][0]['text'].strip()
        await update.message.reply_text(bot_response)
    except Exception as e:
        await update.message.reply_text("مشکلی پیش اومد. لطفاً دوباره امتحان کن.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"یه خطا رخ داده: {context.error}")
    await update.message.reply_text("یه مشکلی پیش اومد.")

# ایجاد بات تلگرام
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# هندلرها
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# مدیریت خطا
app.add_error_handler(error_handler)

# اجرای بات
app.run_polling()
