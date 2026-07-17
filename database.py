from pymongo import MongoClient

# Remplace par ta chaîne de connexion MongoDB (la même que pour tes autres bots)
MONGO_URI = "TA_CHAINE_DE_CONNEXION_MONGODB_ICI"
client = MongoClient(MONGO_URI)

# Nom de la base de données et de la collection pour ce nouveau bot
db = client["bot_crash_aviator_db"]
collection = db["utilisateurs"]

def est_valide(user_id):
    user = collection.find_one({"user_id": str(user_id)})
    if user:
        return user.get("valide", False)
    return False

def ajouter_en_attente(user_id, id_compte):
    collection.update_one(
        {"user_id": str(user_id)},
        {"$set": {"id_compte": id_compte, "valide": False}},
        upsert=True
    )
