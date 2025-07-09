from django.shortcuts import render

from pejy_fandraisana.forms import SentenceCompletionForm
from pejy_fandraisana.gemini_api import chat_with_gemini
from .models import Ohabolana, Sokajy

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
            # Récupérer la phrase partielle
            andian_teny_tsy_feno = form.cleaned_data['partial_sentence']
            
            # Appeler la fonction pour obtenir une complétion
            valiny = chat_with_gemini(andian_teny_tsy_feno)
            
            # Rendre le template avec la réponse
            return render(request, 'pejy_fandraisana/complete_sentence.html', {
                'form': form,
                'valiny': valiny,
                'andian_teny_tsy_feno': andian_teny_tsy_feno
            })
    else:
        form = SentenceCompletionForm()
    
    return render(request, 'pejy_fandraisana/complete_sentence.html', {'form': form})

def pejykabary(request):
    return render(request, 'pejy_fandraisana/kabary.html')