from django.contrib import admin
from .models import Presta, PrestaModificationLog

@admin.register(Presta)
class PrestaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'type', 'numero', 'localisation', 'modified_by')
    search_fields = ('nom', 'ville', 'type')
    list_filter = ('ville', 'type')
    ordering = ('nom',)

    def save_model(self, request, obj, form, change):
        """ Enregistre l'utilisateur qui modifie l'objet et crée un log """
        obj.modified_by = request.user  # Forcer l'utilisateur
        action = "Modification" if change else "Ajout"

        obj.save()  # Sauvegarde de l'objet principal

        # Créer un log d'audit
        PrestaModificationLog.objects.create(
            presta=obj,
            modified_by=request.user,
            action=action
        )

@admin.register(PrestaModificationLog)
class PrestaModificationLogAdmin(admin.ModelAdmin):
    list_display = ('presta', 'modified_by', 'action', 'timestamp')
    search_fields = ('presta__nom', 'modified_by__username', 'action')
    ordering = ('-timestamp',)