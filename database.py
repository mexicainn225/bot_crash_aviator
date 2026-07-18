import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialisation
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# --- CACHE LOCAL ---
# On stocke les IDs autorisés en mémoire pour éviter de demander à Firebase à chaque fois
authorized_cache = set()

def load_cache():
    """Charge une seule fois tous les utilisateurs autorisés au démarrage."""
    try:
        users = db.collection('users').where('authorized', '==', True).stream()
        for user in users:
            authorized_cache.add(user.id)
        print(f"Cache chargé : {len(authorized_cache)} utilisateurs autorisés.")
    except Exception as e:
        print(f"Erreur chargement cache : {e}")

# Appel unique au démarrage
load_cache()

def is_user_authorized(telegram_id):
    """Vérification ultra-rapide en mémoire (RAM)."""
    return str(telegram_id) in authorized_cache

def authorize_user(telegram_id):
    """Valide dans Firebase ET met à jour le cache instantanément."""
    try:
        db.collection('users').document(str(telegram_id)).set({
            'authorized': True,
            'date_validation': firestore.SERVER_TIMESTAMP
        })
        # Mise à jour du cache local
        authorized_cache.add(str(telegram_id))
        print(f"Utilisateur {telegram_id} validé et ajouté au cache.")
    except Exception as e:
        print(f"Erreur validation : {e}")
