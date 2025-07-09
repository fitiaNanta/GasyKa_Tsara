import os
import django
import fitz  # pymupdf

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

from pejy_fandraisana.models import ArticleKolontsaina  # adapte selon ton app

# Ouvrir le fichier PDF
pdf_path = "media/pdfs/kolontsaina.pdf"  # adapte si ton fichier est ailleurs
doc = fitz.open(pdf_path)

contenu_total = ""
for page in doc:
    contenu_total += page.get_text()

# Diviser le texte en parties si tu veux les séparer par sections
# Par exemple, ici on le met dans un seul champ
ArticleKolontsaina.objects.create(
    titre="Kolontsaina Malagasy",
    contenu=contenu_total
)

print("✅ Données insérées dans la base avec succès.")
