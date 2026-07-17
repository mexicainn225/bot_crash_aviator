import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import database

# Token du bot @SIGNAL_COK225bot
TOKEN = "8741779645:AAERPPUYcY0flcK-t5oWDoNGFbjvBYUR_30"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Vérification dans la base de données
    if database.est_valide(user_id):
        keyboard = [
            [InlineKeyboardButton("🚀 Lancer CRASH & AVIATOR", web_app=WebAppInfo(url="TON_LIEN_RENDER"))]
        ]
        await update.message.reply_text("✅ Accès validé ! Clique ci-dessous pour jouer :", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("👋 Bienvenue ! Envoie ton ID pour demander ton accès aux jeux.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    id_recu = update.message.text
    # Enregistrement de l'ID en attente de validation
    database.ajouter_en_attente(user_id, id_recu)
    await update.message.reply_text("⏳ ID reçu. J'attends la validation de l'admin.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
