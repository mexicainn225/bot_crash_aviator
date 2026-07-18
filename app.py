import os
import threading
import database
from flask import Flask
from flask_cors import CORS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# --- CONFIGURATION ---
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 5724620019 
PORT = int(os.environ.get("PORT", 8080))

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Bot en ligne"

# --- LOGIQUE DU BOT ---
async def start(update, context):
    user_id = update.effective_user.id
    if database.is_user_authorized(user_id):
        keyboard = [[InlineKeyboardButton("🚀 Lancer l'Application", web_app={"url": "https://bot-crash-aviator.onrender.com"})]]
        await update.message.reply_text("Accès autorisé, bienvenue !", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("Inscris-toi avec le code COK225 et envoie ton ID pour validation.")

async def handle_message(update, context):
    text = update.message.text
    if text.isdigit() and len(text) > 5:
        await context.bot.send_message(ADMIN_ID, f"🚨 Nouvelle demande ID : {text}\nValide avec: /valider {update.effective_user.id}")
        await update.message.reply_text("ID reçu, attente de validation par l'admin ✅")

async def valider(update, context):
    if update.effective_user.id == ADMIN_ID and context.args:
        user_id_to_auth = context.args[0]
        database.authorize_user(user_id_to_auth)
        await update.message.reply_text(f"Utilisateur {user_id_to_auth} validé !")
        await context.bot.send_message(chat_id=int(user_id_to_auth), text="✅ Ton accès est validé ! Tape /start pour lancer.")

def run_bot():
    """Fonction dédiée au démarrage du bot Telegram."""
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('valider', valider))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

# --- LANCEMENT ---
if __name__ == '__main__':
    # On lance le bot dans un thread séparé
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Flask tourne dans le thread principal (attendu par Gunicorn)
    app.run(host='0.0.0.0', port=PORT)
