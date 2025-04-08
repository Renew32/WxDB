from django.shortcuts import render

# Create your views here.
import openpyxl
from .models import Presta
from rest_framework import viewsets
from .serializers import PrestaSerializer
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm
from django.core.exceptions import ValidationError
from datetime import datetime



def list_presta(request):
    prestataires = Presta.objects.filter(is_deleted=False)

    ville_unique = Presta.objects.filter(is_deleted=False).values_list('ville', flat=True).distinct().order_by('ville')
    type_unique = Presta.objects.filter(is_deleted=False).values_list('type', flat=True).distinct().order_by('type')


   # Nettoyer et supprimer les doublons manuellement
    ville_unique = list(set(v.strip().lower().capitalize() for v in ville_unique if v))
    type_unique = list(set(t.strip().lower().capitalize() for t in type_unique if t))


    return render(request, 'presta/liste_presta.html', {'prestataires': prestataires, 'villes_uniques': ville_unique, 'types_uniques': type_unique}, )



class PrestaViewSet(viewsets.ModelViewSet):
    queryset = Presta.objects.all()
    serializer_class = PrestaSerializer




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Si l'URL "next" est définie, rediriger vers cette page
            next_url = request.GET.get('next', '/admin/')
            return redirect(next_url)
        else:
            messages.error(request, "Identifiants invalides.")
    
    return render(request, 'presta/con.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()

                
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, "Inscription réussie ! Veuillez attendre validation des administrateurs.")
                    return redirect('login_view')
                else:
                    messages.error(request, "Erreur lors de l'authentification. Veuillez réessayer.")
            except ValidationError as e:
                messages.error(request, f"Erreur de validation : {e}")
        else:
            # Gestion des erreurs spécifiques
            
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'presta/register.html', {'form': form})

def export_presta_to_excel(request):
    """ Exporte les données de la table Presta dans un fichier Excel. """

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prestataires"

    headers = ["ID", "Nom", "Ville", "Type", "Numéro", "Latitude", "Longitude", "Localisation", "Supprimé"]
    ws.append(headers)

    prestataires = Presta.objects.all().values_list(
        'id', 'nom', 'ville', 'type', 'numero', 'latitude', 'longitude', 'localisation', 'is_deleted'
    )

    for presta in prestataires:
        ws.append(list(presta[:-1]) + ["Oui" if presta[-1] else "Non"])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    date_str = datetime.now().strftime("%Hh-%Mmin_%d-%m-%y")
    response['Content-Disposition'] = f'attachment; filename="Prestataires_Soins_Chanas_{date_str}.xlsx"'
    wb.save(response)

    return response

