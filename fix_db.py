import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registry_app.settings')
django.setup()

def fix():
    with connection.cursor() as cursor:
        # 1. Create dummy core_userprofile if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS core_userprofile (id bigserial PRIMARY KEY, insurance_id varchar(30), user_id integer)")
        print("Ensured core_userprofile exists.")

        # 2. Drop other tables to ensure 0002 can create them
        tables = [
            'core_partyidentifiertype',
            'core_partyroletype',
            'core_client',
            'core_party',
            'core_partyidentifier',
            'core_partyrole'
        ]
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            print(f"Dropped {table}")

        # 3. Ensure django_migrations only has 0001 for core
        cursor.execute("DELETE FROM django_migrations WHERE app = 'core' AND name != '0001_initial'")
        print("Cleaned up django_migrations for core.")

if __name__ == '__main__':
    fix()
