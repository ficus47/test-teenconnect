import os

def count_characters_in_file(file_path):
    total_chars = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            total_chars = len(file.read())
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
    return total_chars

def count_characters_in_directory(directory):
    total_chars = 0
    # Change to the target directory
    os.chdir(directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            total_chars += count_characters_in_file(file_path)
    return total_chars

if __name__ == "__main__":
    dossier_cible = input("Entrez le chemin du dossier à analyser: ")
    total_caracteres = count_characters_in_directory(dossier_cible)
    print(f"Le nombre total de caractères dans le dossier '{dossier_cible}' est de: {total_caracteres}")
