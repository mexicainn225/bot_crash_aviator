import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import database

# Récupère le TOKEN depuis les variables d'environnement de Render
TOKEN = os.environ.get("TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Test simple pour vérifier la connexion à la base
    await update.message.reply_text(f"Bot opérationnel pour l'ID : {user_id}")

if __name__ == '__main__':
    if not TOKEN:
        print("Erreur : Le TOKEN n'est pas configuré dans les variables d'environnement.")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.run_polling()
