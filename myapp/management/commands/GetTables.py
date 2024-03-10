from django.core.management.base import BaseCommand
from django.db import connection

class Commande(BaseCommand):
    help = 'Retrieve table names and their create table statements'
    
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE' AND table_schema = DATABASE()
            """)
            table_names = cursor.fetchall()

            if not table_names:
                self.stdout.write("No tables found in the database.")
                return

            for table_name in table_names:
                cursor.execute(f"SHOW CREATE TABLE {table_name[0]}")
                create_table_statement = cursor.fetchone()[1]
                self.stdout.write(f"Table: {table_name[0]}\n{create_table_statement}\n")
