import logging
import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler
import database

TOKEN = os.environ.get("TOKEN")
app = Flask(__name__)

# Route simple pour dire à Render : "Je suis bien ouvert sur un port"
@app.route('/')
def home():
    return "Bot en ligne"

# Fonction pour lancer le serveur web
def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Ton code bot existant
async def start(update, context):
    await update.message.reply_text("Bot opérationnel !")

if __name__ == '__main__':
    # Lance le serveur web dans un fil séparé (thread)
    threading.Thread(target=run_web).start()
    
    # Lance le bot
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
