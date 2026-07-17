import firebase_admin
from firebase_admin import credentials, firestore

# Assure-toi que le nom du fichier JSON ici correspond exactement au nom du fichier dans ton dossier
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Tu pourras ajouter tes fonctions ici plus tard
print("Connexion à Firebase réussie !")
