from django.shortcuts import render

from pejy_fandraisana.forms import SentenceCompletionForm
from pejy_fandraisana.gemini_api import chat_with_gemini
from .models import ArticleKolontsaina, Ohabolana, Sokajy

# Create your views here.

def pejyfandraisana(request):
    return render(request, "pejy_fandraisana/fandraisana.html")

def pejytantara(request):
    return render(request, "pejy_fandraisana/tantara.html")

def pejyvohambolana(requst):
    return render(requst, "pejy_fandraisana/vohambolana.html")

def pejyohabolana(request):
    sokajy_lisitra = Sokajy.objects.all()
    ohabolana_lisitra = Ohabolana.objects.all()
    return render(request, "pejy_fandraisana/ohabolana.html", {
        'sokajy-lisitra':sokajy_lisitra,
        'ohabolana_lisitra':ohabolana_lisitra 
        })

def complete_sentence(request):
    if request.method == 'POST':
        form = SentenceCompletionForm(request.POST)
        if form.is_valid():
            # Récupérer l'entrée de l'utilisateur
            user_input = form.cleaned_data['partial_sentence']
            
            # Appeler la fonction pour obtenir une réponse
            valiny = chat_with_gemini(user_input)
            
            # Rendre le template avec la réponse
            return render(request, 'pejy_fandraisana/complete_sentence.html', {
                'form': form,
                'valiny': valiny,
                'user_input': user_input
            })
    else:
        form = SentenceCompletionForm()
    
    return render(request, 'pejy_fandraisana/complete_sentence.html', {'form': form})

def pejykabary(request):
    return render(request, 'pejy_fandraisana/kabary.html')

def pejykolontsaina(request):
    article = ArticleKolontsaina.objects.all()
    context = {
        'pdf_url': '/media/pdfs/kolontsaina.pdf'
    }
    return render(request, 'pejy_fandraisana/kolontsaina.html', context)

def pejysaina(request):
    return render(request, 'pejy_fandraisana/saina.html')