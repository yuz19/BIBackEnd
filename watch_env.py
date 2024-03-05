import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen

class EnvFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Modification détectée dans le fichier .env. Redémarrage du serveur Django...")
        # Redémarrer le serveur Django
    try:
        result = os.system("python manage.py runserver")
        if result != 0:
            print("Une erreur s'est produite lors du démarrage du serveur Django.")
    except Exception as e:
        print("Une erreur s'est produite :", e)

             

if __name__ == "__main__":
    print("Observation du fichier .env pour les modifications...")
    # Créer un observateur pour surveiller les modifications du fichier .env
    observer = Observer()
    observer.schedule(EnvFileHandler(), path='.', recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
