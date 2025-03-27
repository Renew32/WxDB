from django.db import models

# Create your models here.

class Presta(models.Model):
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    numero = models.TextField(max_length=255)
    localisation = models.TextField(max_length=255)

    def __str__(self):
        return self.nom
    
    # test 
    
    def get_google_maps_url(self):
        params = {
            "api": 1,
            "destination": f"{self.nom}, {self.ville}"
        }
        return f"https://www.google.com/maps/dir/?{urlencode(params)}"