from django.contrib import admin

# Register your models here.
from .models import Presta
@admin.register(Presta)
class PrestaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'type', 'numero', 'localisation')  # Affichage dans l'admin
    search_fields = ('nom', 'ville', 'type')  # Recherche
    list_filter = ('ville', 'type')  # Filtres
    ordering = ('nom',)