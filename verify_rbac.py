#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registry_app.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Client, Party, PartyRole, PartyRoleType

def check_user_role(username):
    print(f"\n=== Checking role for user: {username} ===")
    try:
        user = User.objects.get(username=username)
        print(f"  User found: {user.id} - {user.username}")
        
        client = Client.objects.get(user=user)
        print(f"  Client found: {client.client_id} - {client.name}")
        
        party = Party.objects.filter(client_id=client).first()
        if party:
            print(f"  Party found: {party.party_id} - {party.display_name} (type: {party.party_type})")
            
            party_role = PartyRole.objects.filter(party_id=party, status=1).first()
            if party_role:
                print(f"  PartyRole found: {party_role.role_id} - role_type_id: {party_role.role_type_id}")
                
                role_type = PartyRoleType.objects.filter(role_type_id=party_role.role_type_id).first()
                if role_type:
                    print(f"  RoleType found: {role_type.role_type_code} - {role_type.role_type_description}")
                else:
                    print(f"  ERROR: No RoleType found for role_type_id={party_role.role_type_id}")
            else:
                print(f"  ERROR: No PartyRole found for party_id={party.party_id} with status=1")
        else:
            print(f"  ERROR: No Party found for client_id={client.client_id}")
    except User.DoesNotExist:
        print(f"  ERROR: User '{username}' not found")
    except Client.DoesNotExist:
        print(f"  ERROR: Client not found for user '{username}'")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == '__main__':
    check_user_role('insured_user')
    check_user_role('employer_user')
