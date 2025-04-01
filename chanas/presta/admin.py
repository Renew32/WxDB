from django.contrib import admin
from .models import Presta, PrestaModificationLog

@admin.register(Presta)
class PrestaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'type', 'numero', 'localisation', 'is_deleted')
    search_fields = ('nom', 'ville', 'type')
    list_filter = ('ville', 'type', 'is_deleted')
    ordering = ('nom',)
    readonly_fields = ('modified_by',)


    def get_readonly_fields(self, request, obj=None):
        """ Rend le champ 'is_deleted' modifiable uniquement par le superadmin """
        if not request.user.is_superuser:
            return self.readonly_fields + ('is_deleted',)  # Ajoute is_deleted en lecture seule
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
        
        action = "Modification" if change else "Ajout"
        changed_fields = {
            field: {
                'old': form.initial.get(field),
                'new': form.cleaned_data.get(field)
            }
            for field in form.changed_data
        }
        
        PrestaModificationLog.log_action(
            presta=obj,
            user=request.user,
            action=action,
            details={
                'champs_modifies': changed_fields,
                'via': 'Interface admin'
            }
        )

    def delete_model(self, request, obj):
        """Utilise la suppression logique plutôt que physique"""
        obj.delete()  # Appelle la méthode delete() override du modèle


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        existing_types = Presta.objects.values_list('type', flat=True).distinct()
        form.base_fields['type'].choices = [(t, t) for t in existing_types]
        return form


@admin.register(PrestaModificationLog)
class PrestaModificationLogAdmin(admin.ModelAdmin):
    list_display = ('presta', 'modified_by', 'action', 'timestamp',)
    search_fields = ('presta__nom', 'modified_by__username', 'action')
    ordering = ('-timestamp',)
    readonly_fields = ('presta', 'modified_by', 'action', 'timestamp', 'formatted_details')
    list_filter = ('action', 'timestamp')


    def formatted_details(self, obj):
        if obj.details:
            return '\n'.join(f'{k}: {v}' for k, v in obj.details.items())
        return 'Aucun détail'
    formatted_details.short_description = 'Détails formatés'
