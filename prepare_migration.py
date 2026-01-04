import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registry_app.settings')
django.setup()

def prepare_status_migration():
    tables = [
        'core_party',
        'core_partyrole',
        'core_partyroletype',
        'core_partyidentifier',
        'core_partyidentifiertype',
        'core_person'
    ]
    with connection.cursor() as cursor:
        for table in tables:
            try:
                cursor.execute(f"UPDATE {table} SET status = '1' WHERE status = 'A'")
                print(f"Updated {table} status 'A' -> '1'")
            except Exception as e:
                print(f"Could not update {table}: {e}")

if __name__ == '__main__':
    prepare_status_migration()
