import os

USERS_FILE = "users.txt"

def load_authorized_users():
    """Charge les utilisateurs autorisés depuis le fichier local au démarrage."""
    if not os.path.exists(USERS_FILE):
        return set()
    with open(USERS_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

# Chargement initial dans la RAM
authorized_cache = load_authorized_users()
print(f"Cache chargé : {len(authorized_cache)} utilisateurs autorisés.")

def is_user_authorized(telegram_id):
    """Vérification ultra-rapide en mémoire (RAM)."""
    return str(telegram_id) in authorized_cache

def authorize_user(telegram_id):
    """Valide dans le fichier local ET met à jour le cache."""
    uid = str(telegram_id)
    if uid not in authorized_cache:
        authorized_cache.add(uid)
        with open(USERS_FILE, "a") as f:
            f.write(uid + "\n")
        print(f"Utilisateur {uid} validé et sauvegardé.")
