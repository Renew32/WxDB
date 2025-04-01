from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlencode


class Presta(models.Model):
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    localisation = models.TextField(max_length=500, blank=True, null=True)
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Prestataire"
        verbose_name_plural = "Prestataires"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_google_maps_url(self):
            """Génère un lien Google Maps vers la destination"""
            if self.latitude and self.longitude:
                params = {
                    "api": 1,
                    "destination": f"{self.latitude},{self.longitude}"
                }
                return f"https://www.google.com/maps/dir/?{urlencode(params)}"
            return "Coordonnées GPS non disponibles"

    def delete(self, *args, **kwargs):
        """Override de la méthode delete pour une suppression logique"""
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):
        """Surcharge la méthode save pour stocker le lien Google Maps"""
        if self.latitude is not None and self.longitude is not None:
            self.localisation = self.get_google_maps_url()
        else:
            self.localisation = None

        super(Presta, self).save(*args, **kwargs)  # Appel à la méthode save() de la classe parent

class PrestaModificationLog(models.Model):
    presta = models.ForeignKey(
        Presta, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Log de modification"
        verbose_name_plural = "Logs de modifications"
        ordering = ['-timestamp']

    def __str__(self):
        presta_name = self.presta.nom if self.presta else "[Presta supprimé]"
        username = self.modified_by.username if self.modified_by else "[Utilisateur inconnu]"
        return f"{self.action} - {presta_name} par {username} à {self.timestamp}"

    @classmethod
    def log_action(cls, presta, user, action, details=None):
        """Méthode helper pour logger une action"""
        return cls.objects.create(
            presta=presta,
            modified_by=user,
            action=action,
            details=details or {}
        )