from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from presta.models import Presta  # Modèle à surveiller
from .models import PrestaModificationLog

@receiver(pre_save, sender=Presta)  # Remplace "Presta" par le modèle à suivre
def log_presta_modification(sender, instance, **kwargs):
    if instance.pk:  # Vérifie si l'objet existe déjà (modification et non création)
        try:
            old_instance = Presta.objects.get(pk=instance.pk)
            for field in instance._meta.fields:
                field_name = field.name
                old_value = getattr(old_instance, field_name)
                new_value = getattr(instance, field_name)

                if old_value != new_value:  # Si une modification a eu lieu
                    PrestaModificationLog.objects.create(
                        admin_user=instance.modified_by,  # Qui a fait la modification
                        model_name=sender.__name__,
                        object_id=instance.pk,
                        field_name=field_name,
                        old_value=old_value,
                        new_value=new_value,
                    )
        except Presta.DoesNotExist:
            pass  # Si l'objet n'existe pas encore, ne rien faire