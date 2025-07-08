from django.shortcuts import render
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

