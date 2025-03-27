from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlencode  # ✅ Import ajouté

# Create your models here.

class Presta(models.Model):
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    numero = models.TextField(max_length=255)
    localisation = models.TextField(max_length=255)
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # Admin qui modifie

    def __str__(self):
        return self.nom

    def get_google_maps_url(self):
        """Génère un lien Google Maps vers l'adresse de l'entreprise"""
        params = {
            "api": 1,
            "destination": f"{self.nom}, {self.ville}"
        }
        return f"https://www.google.com/maps/dir/?{urlencode(params)}"


class PrestaModificationLog(models.Model):
    presta = models.ForeignKey(Presta, on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)  # "Ajout", "Modification"
    timestamp = models.DateTimeField(auto_now_add=True)  # Date et heure de la modification

    def __str__(self):
        return f'{self.action} on {self.presta.nom} by {self.modified_by} at {self.timestamp}'