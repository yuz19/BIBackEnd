from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Generate models from the existing database schema'

    def handle(self, *args, **options):
        # Call the inspectdb command to generate models
        with open("models.py", "w") as f:
            call_command('inspectdb', stdout=f)
