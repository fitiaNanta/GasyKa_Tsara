import re

def garder_phrase(texte):
    # Garder seulement les caractères autorisés pour une phrase basique
    return re.sub(r"[^a-zA-Z0-9\s.,!?':;\"-]", "", texte)

# Exemple sur un fichier CSV, colonne par colonne
import csv

input_path = '/run_results2.csv'
output_path = '/mnt/data/run_results2_filtré.csv'

with open(input_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8', newline='') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    for row in reader:
        # filtrer chaque cellule de la ligne
        new_row = [garder_phrase(cell) for cell in row]
        writer.writerow(new_row)

print(f"Fichier filtré créé ici : {output_path}")
