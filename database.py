import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- INITIALISATION ---
# Assure-toi que le fichier serviceAccountKey.json est à la racine de ton projet
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

print("Connexion à Firebase réussie !")

# --- FONCTIONS DE GESTION DES UTILISATEURS ---

def is_user_authorized(telegram_id):
    """
    Vérifie si l'ID Telegram est présent dans la collection 'users' 
    et si le champ 'authorized' est égal à True.
    """
    try:
        doc_ref = db.collection('users').document(str(telegram_id))
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict().get('authorized', False)
        return False
    except Exception as e:
        print(f"Erreur lors de la vérification de l'utilisateur : {e}")
        return False

def authorize_user(telegram_id):
    """
    Ajoute ou met à jour l'ID Telegram dans la collection 'users'.
    Définit le statut 'authorized' à True.
    """
    try:
        db.collection('users').document(str(telegram_id)).set({
            'authorized': True,
            'date_validation': firestore.SERVER_TIMESTAMP
        })
        print(f"Utilisateur {telegram_id} validé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la validation de l'utilisateur : {e}")
