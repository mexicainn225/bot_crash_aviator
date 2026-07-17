import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import database

# Ton TOKEN
TOKEN = "8741779645:AAERPPUYcY0flcK-t5oWDoNGFbjvBYUR_30"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Test simple pour vérifier la connexion à la base
    await update.message.reply_text(f"Bot opérationnel pour l'ID : {user_id}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
