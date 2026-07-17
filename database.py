import firebase_admin
from firebase_admin import credentials, firestore

# Initialisation de Firebase
cred = credentials.Certificate("serviceAccountKey.json") # Assure-toi d'avoir ce fichier dans ton repo
firebase_admin.initialize_app(cred)
db = firestore.client()

# Nom de la collection pour ce nouveau bot
COLLECTION = "utilisateurs_crash_aviator"

def est_valide(user_id):
    user_ref = db.collection(COLLECTION).document(str(user_id)).get()
    if user_ref.exists:
        return user_ref.to_dict().get("valide", False)
    return False

def ajouter_en_attente(user_id, id_compte):
    db.collection(COLLECTION).document(str(user_id)).set({
        "id_compte": id_compte,
        "valide": False
    })
