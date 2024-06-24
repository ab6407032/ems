from django.core.management.base import BaseCommand
from helpers import load_file_contents_db, calculate_scores
import os
from django.core.management.base import BaseCommand
from monitor.models import RouterLogFile
from django.conf import settings

class Command(BaseCommand):
    help = 'Check for new files in the uploads folder and create an entry in RouterLogFile model'

    def handle(self, *args, **kwargs):
        folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        for filename in os.listdir(folder_path):
            file = RouterLogFile.objects.filter(name__contains=filename)
            if not file.exists():
                file_path = os.path.join(folder_path, filename)
                self.create_router_log_file_entry(file_path, filename)
        load_file_contents_db()
        calculate_scores()

    def create_router_log_file_entry(self, file_path, filename):
        # Create a new RouterLogFile entry
        RouterLogFile.objects.create(file=file_path, name=filename, processed=False)
        self.stdout.write(self.style.SUCCESS(f'Processed new file: {filename}'))