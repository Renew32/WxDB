from django.shortcuts import render

# Create your views here.
from .models import presta
from rest_framework import viewsets
from .serializers import PrestaSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def list_presta(request):
    prestataires = presta.objects.all()

    ville_unique = presta.objects.values_list('ville', flat=True).distinct().order_by('ville')
    type_unique = presta.objects.values_list('type', flat=True).distinct().order_by('type')


   # Nettoyer et supprimer les doublons manuellement
    ville_unique = list(set(v.strip().lower().capitalize() for v in ville_unique if v))
    type_unique = list(set(t.strip().lower().capitalize() for t in type_unique if t))


    return render(request, 'presta/liste_presta.html', {'prestataires': prestataires, 'villes_uniques': ville_unique, 'types_uniques': type_unique} )



class PrestaViewSet(viewsets.ModelViewSet):
    queryset = presta.objects.all()
    serializer_class = PrestaSerializer




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirection vers la page d'accueil après connexion
        else:
            messages.error(request, "Adresse e-mail ou mot de passe incorrect.")

    return render(request, 'presta/con.html')