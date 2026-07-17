import logging
import os
import threading
import random
from flask import Flask, jsonify
from flask_cors import CORS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from datetime import datetime
import database

# --- CONFIGURATION ---
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 5724620019 
app = Flask(__name__)
CORS(app)

# --- PARTIE WEB ---
@app.route('/')
def home():
    return "Bot en ligne"

@app.route('/get_signal/<game>')
def get_signal(game):
    # Logique signal identique...
    return jsonify({'status': 'ok'})

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# --- PARTIE BOT TELEGRAM ---
async def start(update, context):
    user_id = update.effective_user.id
    if database.is_user_authorized(user_id):
        keyboard = [[InlineKeyboardButton("🚀 Lancer l'Application", web_app={"url": "https://bot-crash-aviator.onrender.com"})]]
        await update.message.reply_text("Accès autorisé :", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("Inscris-toi avec le code COK225 et envoie ton ID.")

async def handle_message(update, context):
    text = update.message.text
    if text.isdigit() and len(text) > 5:
        database.db.collection('pending_ids').document(str(update.effective_user.id)).set({
            'telegram_id': update.effective_user.id,
            'id_1xbet': text,
            'status': 'en_attente'
        })
        await context.bot.send_message(ADMIN_ID, f"Nouvel ID : {text}")
        await update.message.reply_text("ID reçu, attente validation ✅")

async def valider(update, context):
    if update.effective_user.id == ADMIN_ID and context.args:
        database.authorize_user(context.args[0])
        await update.message.reply_text("Validé !")

# --- LANCEMENT ---
if __name__ == '__main__':
    # On lance Flask dans un thread séparé
    threading.Thread(target=run_flask, daemon=True).start()
    
    # On lance le bot dans le thread principal
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('valider', valider))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()
