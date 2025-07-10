import google.generativeai as genai
import pdfplumber
import os
from django.conf import settings
from django.db.models import Q
from pejy_fandraisana.models import Ohabolana, ArticleKolontsaina
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configurez votre clé API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyC15PyLpKjHZPRPmqdxS2LYzbZKYQPQWIE")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialisez le modèle
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text_from_pdfs(pdf_dir):
    """
    Manala ny lahatsoratra avy amin'ny rakitra PDF rehetra ao amin'ny lahatahiry voafaritra.
    """
    text = ""
    try:
        for filename in os.listdir(pdf_dir):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(pdf_dir, filename)
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
        if not text.strip():
            return "Tsy nahomby: Tsy nisy lahatsoratra nalaina tamin'ny PDF."
        return text
    except Exception as e:
        return f"Tsy nahomby ny fanesorana ny lahatsoratra: {e}"

def search_in_database(keywords):
    """
    Mikaroka ao amin'ny base de données mifototra amin'ny teny fanalahidy.
    """
    try:
        # Recherche dans Ohabolana
        ohabolana_results = Ohabolana.objects.filter(
            Q(ohabolana__icontains=keywords) | Q(mpanoratra__icontains=keywords)
        )
        ohabolana_text = "\n".join([f"- {o.ohabolana} (Mpanoratra: {o.mpanoratra})" for o in ohabolana_results])

        # Recherche dans ArticleKolontsaina
        article_results = ArticleKolontsaina.objects.filter(
            Q(titre__icontains=keywords) | Q(contenu__icontains=keywords)
        )
        article_text = "\n".join([f"- {a.titre}: {a.contenu[:200]}..." for a in article_results])

        if not ohabolana_text and not article_text:
            return "Tsy nahitana valiny mifanaraka amin'ny teny fanalahidy."
        return f"**Ohabolana**:\n{ohabolana_text}\n\n**Article Kolontsaina**:\n{article_text}"
    except Exception as e:
        return f"Tsy nahomby ny fikarohana: {e}"

def chat_with_gemini(user_input):
    """
    Mifandray amin'ny Gemini API mba hamenoana ohabolana na hifampiresahana amin'ny teny malagasy.
    """
    try:
        # Liste de mots-clés pour détecter une demande de complétion d'ohabolana
        completion_keywords = ["mameno", "ohabolana", "feno", "fenoy", "hameno"]
        is_completion_request = any(keyword in user_input.lower() for keyword in completion_keywords)

        if is_completion_request:
            # Extraire le texte des PDFs pour la complétion d'ohabolana
            pdf_text = extract_text_from_pdfs(settings.PDF_DIR)
            if "Tsy nahomby" in pdf_text:
                return pdf_text

            # Prompt pour la complétion d'ohabolana
            prompt = (
                f"Ianao dia manam-pahaizana amin'ny teny malagasy. Ny asanao dia ny mameno andian-teny tsy feno araka ny fomba sy ny votoatin'ny antontan-taratasy manaraka. "
                f"Ampiasao ny fomba voajanahary sy hajao ny fitenenana malagasy mahazatra.\n\n"
                f"**Votoatin'ny antontan-taratasy** : {pdf_text}\n\n"
                f"**Ohatra** :\n"
                f"- Andian-teny tsy feno : 'Ny fanambadiana toy ny jiafotsy'\n"
                f"  Famenoana : 'Ny fanambadiana toy ny jiafotsy, vao tsy ialan-kasokasoka, tonta tsy ialan-dromoromo'\n"
                f"- Andian-teny tsy feno : 'Ny fitiavana toy ny'\n"
                f"  Famenoana : 'Ny fitiavana toy ny rano madio, mangarahara fa sarotra hotazonina'\n\n"
                f"**Andian-teny tsy feno hamenoana** : {user_input}\n"
                f"Mamenoa ny andian-teny araka ny fomba sy ny votoatin'ny antontan-taratasy ary amin'ny teny malagasy."
            )
        else:
            # Recherche dans la base de données pour une conversation générale
            keywords = user_input  # Vous pouvez ajouter un traitement NLP ici pour extraire des mots-clés pertinents
            db_results = search_in_database(keywords)

            # Prompt pour une conversation générale
            prompt = (
                f"Ianao dia mpifampiresaka amin'ny teny malagasy. Valio amin'ny teny malagasy voajanahary sy mahalala fomba. "
                f"Araka ny fangatahan'ny mpampiasa sy ny votoatin'ny base de données, omeo valiny mifanaraka.\n\n"
                f"**Fangatahan'ny mpampiasa** : {user_input}\n\n"
                f"**Votoatin'ny base de données** : {db_results}\n\n"
                f"Valio amin'ny teny malagasy, mifototra amin'ny votoatin'ny base de données raha ilaina, ary raha tsy misy fampahalalana mifanaraka, omeo valiny ankapobeny nefa mbola mifandraika amin'ny kolontsaina malagasy."
            )

        # Appeler l'API Gemini
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Tsy nahomby ny famokarana valiny: {e}"