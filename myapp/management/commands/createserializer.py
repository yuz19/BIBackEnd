import os
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework import serializers

class Command(BaseCommand):
    help = 'Generate a single serializer file for all models in the app'

    def handle(self, *args, **options):
        app_name = 'myapp'  # Replace 'myapp' with your application name
        app_config = apps.get_app_config(app_name)
        models = list(app_config.get_models())  # Convert generator to list

        BASE_DIR = settings.BASE_DIR

        serializer_file_name = 'serializers.py'
        serializer_path = os.path.join(BASE_DIR, 'myapp', serializer_file_name)

        with open(serializer_path, 'w') as serializer_file:
            serializer_file.write("from rest_framework import serializers\n")
            serializer_file.write("from .models import (\n")

            for model in models:
                model_name = model.__name__
                serializer_file.write(f"    {model_name},\n")
                
            serializer_file.write(")\n\n")
            print(f"Number of models: {len(models)}")  # Now this should work

            for model in models: 
                print("Inside second loop")  # Debug print
                model_name = model.__name__
                serializer_name = f"{model_name}Serializer"
                serializer_fields = [field.name for field in model._meta.fields]
                serializer_file.write(f"class {serializer_name}(serializers.ModelSerializer):\n")
                serializer_file.write(f"    class Meta:\n")
                serializer_file.write(f"        model = {model_name}\n")
                serializer_file.write(f"        fields = {serializer_fields}\n\n")
