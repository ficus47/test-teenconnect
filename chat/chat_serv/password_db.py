import os
from msg_db.msg_db import check_user
from hashlib import sha224

lien = "chat_serv/"#r"C:/Users/Coqen/OneDrive/Bureau/tout_python/chat_serv/"

def hash_password(password):
	password_encoded = password.encode()
	del password
	return sha224(password_encoded).hexdigest()

# Fonction pour vérifier le mot de passe utilisateur
def check_user_password(user, password):
    # Chemin du fichier de l'utilisateur
    user_file_path = os.path.join(lien, "user_password", user)

    # Vérifier si le fichier de l'utilisateur existe
    if os.path.exists(user_file_path):
        # Lire le mot de passe hashé depuis le fichier
        with open(user_file_path, "r") as file:
            stored_password_hash = file.read().strip()
        
        # Comparer les deux hashs
        password_hash = hash_password(password)
        print(stored_password_hash, password_hash, password_hash == stored_password_hash)
        return password_hash == stored_password_hash
    else:
        # Si l'utilisateur n'existe pas, créer son fichier et y écrire le mot de passe hashé
        with open(user_file_path, "w") as file:
            file.write(hash_password(password))
        return False