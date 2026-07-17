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
ADMIN_ID = 5724620019  # Ton ID est intégré ici
app = Flask(__name__)
CORS(app)

# Tes séquences de minutes
sequences = {
    'CRASH': [0, 4, 7, 10, 14, 17, 20, 24, 27, 30, 34, 37, 40, 44, 47, 50, 54, 57],
    'AVIATOR': [3, 5, 9, 13, 15, 19, 23, 25, 29, 33, 35, 39, 43, 45, 49, 53, 55, 59]
}

current_data = {'CRASH': {'cote': 0, 'minute': -1}, 'AVIATOR': {'cote': 0, 'minute': -1}}

# --- PARTIE WEB (API) ---
@app.route('/')
def home():
    return "Bot en ligne"

@app.route('/get_signal/<game>')
def get_signal(game):
    if game not in sequences:
        return jsonify({'error': 'Jeu inconnu'}), 404
        
    now = datetime.now()
    min_actuelle = now.minute
    seq = sequences[game]
    next_min = next((m for m in seq if m >= min_actuelle), seq[0])
    
    if current_data[game]['minute'] != next_min:
        current_data[game]['cote'] = round(random.uniform(1.1, 25.0), 2)
        current_data[game]['minute'] = next_min
        
    return jsonify({'cote': current_data[game]['cote'], 'minute': current_data[game]['minute']})

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# --- PARTIE BOT TELEGRAM ---
async def start(update, context):
    user_id = update.effective_user.id
    
    # Vérification dans la base de données
    if database.is_user_authorized(user_id):
        keyboard = [[InlineKeyboardButton("🚀 Lancer l'Application", web_app={"url": "https://bot-crash-aviator.onrender.com"})]]
        await update.message.reply_text("Re-bonjour ! Voici ton accès :", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        msg = ("Bienvenue sur le bot 1win 🚀\n\n"
               "Pour débloquer tes accès, suis ces étapes :\n\n"
               "1️⃣ Inscris-toi sur 1XBET ici : https://lkbb.cc\n"
               "2️⃣ Utilise le code promo : COK225\n"
               "3️⃣ Effectue une recharge sur ton compte OBLIGATOIRE\n"
               "4️⃣ Envoie ton ID 1XBET ici pour validation.")
        await update.message.reply_text(msg)

async def handle_message(update, context):
    text = update.message.text
    if text.isdigit() and len(text) > 5:
        await context.bot.send_message(ADMIN_ID, f"Nouvelle demande d'accès :\nID : {text}\nUtilisateur : @{update.effective_user.username}")
        await update.message.reply_text("ID reçu ! J'ai transmis ta demande à l'admin. Attends la validation. ✅")

async def valider(update, context):
    if update.effective_user.id == ADMIN_ID:
        if context.args:
            target_id = context.args[0]
            database.authorize_user(target_id)
            await update.message.reply_text(f"Utilisateur {target_id} validé ! Accès débloqué.")

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('valider', valider))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling(drop_pending_updates=True)
