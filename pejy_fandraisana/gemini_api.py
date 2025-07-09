import google.generativeai as genai
import pdfplumber
import os
from django.conf import settings
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configurez votre clé API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyC15PyLpKjHZPRPmqdxS2LYzbZKYQPQWIE")  # Remplacez par votre clé
genai.configure(api_key=GOOGLE_API_KEY)

# Initialisez le modèle
model = genai.GenerativeModel('gemini-1.5-flash')  # Modèle gratuit

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
            return "Tsy nahomby: Tsy nisy lahatsoratra nalaina tamin'ny PDF. Mety ho sary na tsy misy afa-tsy ny antontan-taratasy."
        return text
    except Exception as e:
        return f"Tsy nahomby ny fanesorana ny lahatsoratra: {e}"

def chat_with_gemini(partial_sentence):
    """
    Mameno andian-teny tsy feno mifototra amin'ny votoatin'ny PDF.
    """
    try:
        # Manala ny lahatsoratra avy amin'ny PDF rehetra ao amin'ny PDF_DIR
        pdf_text = extract_text_from_pdfs(settings.PDF_DIR)
        if "Tsy nahomby" in pdf_text:
            return pdf_text
        
        # Mamorona ny prompt amin'ny toromarika sy ohatra
        prompt = (
            f"Ianao dia manam-pahaizana amin'ny teny malagasy. Ny asanao dia ny mameno andian-teny tsy feno araka ny fomba sy ny votoatin'ny antontan-taratasy manaraka. "
            f"Ampiasao ny fomba voajanahary sy hajao ny fitenenana malagasy mahazatra.\n\n"
            f"**Votoatin'ny antontan-taratasy** : {pdf_text}\n\n"
            f"**Ohatra** :\n"
            f"- Andian-teny tsy feno : 'Ny fanambadiana toy ny jiafotsy'\n"
            f"  Famenoana : 'Ny fanambadiana toy ny jiafotsy, vao tsy ialan-kasokasoka, tonta tsy ialan-dromoromo'\n"
            f"- Andian-teny tsy feno : 'Ny fitiavana toy ny'\n"
            f"  Famenoana : 'Ny fitiavana toy ny rano madio, mangarahara fa sarotra hotazonina'\n\n"
            f"**Andian-teny tsy feno hamenoana** : {partial_sentence}\n"
            f"Mamenoa ny andian-teny araka ny fomba sy ny votoatin'ny antontan-taratasy ary amin'ny teny malagasy."
        )
        
        # Miantso ny API
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Tsy nahomby ny famokarana valiny: {e}"