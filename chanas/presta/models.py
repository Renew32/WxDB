from django.db import models

# Create your models here.

class presta(models.Model):
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    numero = models.CharField(max_length=20) 

    def __str__(self):
        return self.nom