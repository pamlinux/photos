import os
import unicodedata
import zipfile

def normalize_filename(filename):
    """Convertit le nom de fichier en NFC (forme composée) pour éviter les erreurs sur macOS."""
    return unicodedata.normalize('NFC', filename)

def get_all_files_in_directory(directory):
    """Retourne une liste de tous les fichiers dans un répertoire (y compris sous-dossiers)."""
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), directory)
            file_list.append(normalize_filename(relative_path.replace("\\", "/")))  # Normalisation des chemins
    return set(file_list)


def get_dirname(number):
    return "/Volumes/Public/Backup Google Photo/takeout-20250223T083631Z-" + str(number).zfill(3)


def get_zipname(number):
    return "/Volumes/Public/Backup Google Photo/takeout-20250223T083631Z-" + str(number).zfill(3) + ".zip"

def get_files_in_zip(zip_path):
    """Retourne une liste de tous les fichiers contenus dans une archive ZIP."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        normalized_zip_files = {normalize_filename(f) for f in zip_ref.namelist()}
        return normalized_zip_files  # Liste des fichiers dans l'archive

def check_google_photos_part(number):
    zip_files = get_files_in_zip(get_zipname(number))
    dir_files = get_all_files_in_directory(get_dirname(number))
    print(f"Pour l'archive {number}, la différence avec le directoire est : {len(zip_files - dir_files)}")

def check_all_google_photos_part():
    for k in range(1,33):
        check_google_photos_part(k)

if __name__ == "__main__":
    check_all_google_photos_part()
