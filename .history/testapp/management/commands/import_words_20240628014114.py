import pandas as pd
from django.core.management.base import BaseCommand
from testapp.models import Word, Test

class Command(BaseCommand):
    help = 'Import words from a CSV or Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV or Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        else:
            self.stdout.write(self.style.ERROR('Unsupported file format'))
            return

        for index, row in data.iterrows():
            word, created = Word.objects.get_or_create(word=row['word'], meaning=row['meaning'])
            self.stdout.write(self.style.SUCCESS(f'Successfully imported: {word.word}'))

        self.stdout.write(self.style.SUCCESS('Import completed successfully'))
