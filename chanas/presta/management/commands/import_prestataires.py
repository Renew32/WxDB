import os
import pandas as pd
import django
from django.core.management.base import BaseCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chanas.settings')
django.setup()

from presta.models import presta

class Command(BaseCommand):
    help = 'Importer les prestataires depuis un fichier Excel'

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(BASE_DIR, 'media', 'prestataire_soins2.xlsx')

        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Fichier introuvable : {file_path}")

            # Lire le fichier Excel
            df = pd.read_excel(file_path)
            self.stdout.write(f"Colonnes détectées: {', '.join(df.columns)}")

            # Vérification des colonnes requises
            required_columns = ['PRESTATAIRES', 'LIEU', 'TYPE', 'TELEPHONE']
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Colonnes manquantes: {', '.join(missing_cols)}")

            # Traitement des données
            success_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    presta.objects.update_or_create(
                        nom=row['PRESTATAIRES'],
                        defaults={
                            'ville': row.get('LIEU', ''),
                            'type': row.get('TYPE', ''),
                            'numero': str(row.get('TELEPHONE', ''))
                        }
                    )
                    success_count += 1
                except Exception as e:
                    errors.append(f"Ligne {index+2}: {str(e)}")
                    continue

            # Rapport d'exécution
            self.stdout.write(self.style.SUCCESS(
                f"Importation terminée : {success_count}/{len(df)} lignes importées avec succès"
            ))
            
            if errors:
                self.stdout.write(self.style.WARNING(
                    f"\nErreurs rencontrées ({len(errors)}):\n" + "\n".join(errors[:5]) + 
                    ("\n..." if len(errors) > 5 else "")
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"ERREUR CRITIQUE: {str(e)}"
            ))