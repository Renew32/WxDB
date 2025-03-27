from django.shortcuts import render

# Create your views here.
from .models import Presta
from rest_framework import viewsets
from .serializers import PrestaSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def list_presta(request):
    prestataires = Presta.objects.all()

    ville_unique = Presta.objects.values_list('ville', flat=True).distinct().order_by('ville')
    type_unique = Presta.objects.values_list('type', flat=True).distinct().order_by('type')


   # Nettoyer et supprimer les doublons manuellement
    ville_unique = list(set(v.strip().lower().capitalize() for v in ville_unique if v))
    type_unique = list(set(t.strip().lower().capitalize() for t in type_unique if t))


    return render(request, 'presta/liste_presta.html', {'prestataires': prestataires, 'villes_uniques': ville_unique, 'types_uniques': type_unique} )



class PrestaViewSet(viewsets.ModelViewSet):
    queryset = Presta.objects.all()
    serializer_class = PrestaSerializer




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Si l'URL "next" est définie, rediriger vers cette page
            next_url = request.GET.get('next', '/admin/')
            return redirect(next_url)
        else:
            messages.error(request, "Identifiants invalides.")
    
    return render(request, 'presta/con.html')

