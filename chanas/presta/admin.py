from django.contrib import admin
from django import forms
from .models import Presta, PrestaModificationLog


class PrestaForm(forms.ModelForm):
    ville = forms.ChoiceField(
        choices=[],
        required=True
    )
    type = forms.ChoiceField(
        choices=[],
        required=True
    )

    class Meta:
        model = Presta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        villes = Presta.objects.values_list('ville', flat=True).distinct()
        types = Presta.objects.values_list('type', flat=True).distinct()

        villes = list(set(t.strip() for t in villes if t))

        types = list(set(t.strip() for t in types if t))



        self.fields['ville'].choices = [('', 'Sélectionnez une ville')] + [(v, v) for v in villes]
        self.fields['type'].choices = [('', 'Sélectionnez un type')] + [(t, t) for t in types]



@admin.register(Presta)
class PrestaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'type', 'numero', 'latitude', 'longitude','localisation', 'is_deleted')
    search_fields = ('nom', 'ville', 'type')
    list_filter = ('ville', 'type', 'is_deleted')
    ordering = ('nom',)
    readonly_fields = ('modified_by', 'localisation')
    form = PrestaForm


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
        def format_value(value):
            """Formate proprement les valeurs, y compris les dictionnaires imbriqués."""
            if isinstance(value, dict):
                return '\n    '.join(f'{sub_k}: {sub_v}' for sub_k, sub_v in value.items())
            return str(value)

        if obj.details:
            return '\n'.join(f"{k.capitalize()}:\n    {format_value(v)}" for k, v in obj.details.items())
        return "Aucun détail disponible."
