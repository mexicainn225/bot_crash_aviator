import logging
import os
import threading
import random
from flask import Flask, jsonify
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime
import database # Assure-toi que ton fichier database.py est bien présent

# --- CONFIGURATION ---
TOKEN = os.environ.get("TOKEN")
app = Flask(__name__)

# Tes séquences de minutes
sequences = {
    'CRASH': [0, 4, 7, 10, 14, 17, 20, 24, 27, 30, 34, 37, 40, 44, 47, 50, 54, 57],
    'AVIATOR': [3, 5, 9, 13, 15, 19, 23, 25, 29, 33, 35, 39, 43, 45, 49, 53, 55, 59]
}

current_data = {'CRASH': {'cote': 0, 'minute': -1}, 'AVIATOR': {'cote': 0, 'minute': -1}}

# --- PARTIE WEB (API POUR L'APP) ---
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
    await update.message.reply_text("Bot opérationnel ! Le serveur de signaux est actif.")

if __name__ == '__main__':
    # 1. Lance le serveur web (Flask) dans un thread séparé
    threading.Thread(target=run_web, daemon=True).start()
    
    # 2. Lance le bot Telegram
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    
    print("Bot et Serveur API lancés avec succès...")
    application.run_polling()
