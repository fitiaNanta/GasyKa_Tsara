import os
import django
import fitz  # PyMuPDF

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

from pejy_fandraisana.models import Ohabolana, Sokajy

# Extraction du texte depuis un fichier PDF
def extraire_texte_pdf(fichier):
    doc = fitz.open(fichier)
    texte_complet = ""
    for page in doc:
        texte_complet += page.get_text()
    return texte_complet

# Découpe des proverbes depuis le texte brut
def parser_proverbes(texte_brut):
    lignes = texte_brut.strip().split("\n")
    proverbes = []
    for i in range(len(lignes)):
        ligne = lignes[i].strip()
        if ligne and ligne[0].isdigit() and "." in ligne:
            texte = ligne.split(".", 1)[1].strip()
            auteur = lignes[i + 1].strip() if i + 1 < len(lignes) else "Anonyme"
            proverbes.append((texte, auteur))
    return proverbes

# Enregistrement dans la base de données
def enregistrer_dans_bdd(proverbes, nom_sokajy="Ady"):
    sokajy_obj, created = Sokajy.objects.get_or_create(anarana=nom_sokajy)
    count = 0
    for texte, auteur in proverbes:
        # Vérifie si le texte existe déjà
        if not Ohabolana.objects.filter(ohabolana=texte).exists():
            Ohabolana.objects.create(
                ohabolana=texte,
                mpanoratra=auteur,
                sokajy=sokajy_obj
            )
            count += 1
    print(f"{count} ohabolana insérés dans la base.")

# Lancer le script
if __name__ == "__main__":
    texte_pdf = extraire_texte_pdf("ady.pdf")
    proverbes = parser_proverbes(texte_pdf)
    enregistrer_dans_bdd(proverbes, nom_sokajy="ady")
