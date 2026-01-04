import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registry_app.settings')
django.setup()

tables = [
    'core_partyidentifiertype',
    'core_partyroletype',
    'core_client',
    'core_party',
    'core_partyidentifier',
    'core_partyrole',
    'core_userprofile'
]

with connection.cursor() as cursor:
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            print(f"Dropped {table}")
        except Exception as e:
            print(f"Error dropping {table}: {e}")

print("Cleanup complete.")
