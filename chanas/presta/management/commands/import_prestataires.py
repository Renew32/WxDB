import pandas as pd
import os
import openpyxl
from django.core.management.base import BaseCommand
from presta.models import presta


class Command(BaseCommand):
    help = 'Importer les prestataires depuis un fichier Excel'

    def handle(self, *args, **kwargs):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(BASE_DIR, 'media', 'prestataire_soins.xlsx')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier '{file_path}' est introuvable.")

        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            presta.objects.create(nom=row['PRESTATATAIRES SANTES'], ville=row['VILLE'], type=row['TYPE'])
        self.stdout.write(self.style.SUCCESS('Importation réussie !'))


