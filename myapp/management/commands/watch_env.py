import os
import sys
import time
from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from importlib import reload

class EnvChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def on_modified(self, event):
        if event.src_path.endswith('.env'):
            self.command.stdout.write("Detected .env file change. Reloading server...\n")
            reload(sys.modules['__main__'])  # Reload the main module
            # Note: This assumes your Django server is launched from the __main__ module.

class Command(BaseCommand):
    help = 'Watches for changes in .env file and reloads the server'

    def handle(self, *args, **options):
        path = '.env'  # Change this to the path of your .env file if it's different
        event_handler = EnvChangeHandler(self)
        observer = Observer()
        observer.schedule(event_handler, path)
        observer.start()
        self.stdout.write(self.style.SUCCESS("Watching for changes in .env file..."))
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
