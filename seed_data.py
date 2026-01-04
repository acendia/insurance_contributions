import os
import django
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registry_app.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Client, Party, PartyRole, PartyRoleType, PartyIdentifier, PartyIdentifierType, Person, Organization, Address, Account, AccountType, AccountTransaction, TransactionObligation, InsuranceContribution, ObligationBalance, PartyRelationship, PartyRelationshipType
from datetime import date, datetime

def seed():
    # 1. Ensure we have a User
    user, created = User.objects.get_or_create(username='seed_user', email='seed@example.com')
    if created:
        user.set_password('password123')
        user.save()
    
    # 2. Ensure we have a Client (since Party depends on it)
    client, created = Client.objects.get_or_create(
        user=user,
        client_id=1,
        defaults={
            'name': 'Default Seed Client',
            'address': 'Main Str 123',
            'phone': '1234567890',
            'email': 'seed@example.com',
            'insurance_id': 'INS-001'
        }
    )

    # 3. Create PartyRoleTypes 'INS' and 'EMP'
    role_types = [
        {'id': 1, 'code': 'INS', 'desc': 'Insured Person'},
        {'id': 2, 'code': 'EMP', 'desc': 'Employer'},
    ]
    for rt in role_types:
        PartyRoleType.objects.get_or_create(
            role_type_id=rt['id'],
            defaults={
                'role_type_code': rt['code'],
                'role_type_description': rt['desc'],
                'status': 1,
                'created_by': 'system',
                'last_updated_by': 'system'
            }
        )

    # 4. Create PartyIdentifierTypes
    identifier_types = [
        {'id': 1, 'code': 'AMA', 'desc': 'Social Security Number (AMA)'},
        {'id': 2, 'code': 'AMKA', 'desc': 'Social Security Identity Number (AMKA)'},
        {'id': 3, 'code': 'AFM', 'desc': 'Tax Identification Number (AFM)'},
        {'id': 4, 'code': 'ADT', 'desc': 'Identity Card Number (ADT)'},
        {'id': 5, 'code': 'AME', 'desc': 'Employer Registry Number (AME)'},
    ]
    
    id_type_objs = {}
    for it in identifier_types:
        obj, created = PartyIdentifierType.objects.get_or_create(
            identifier_type_id=it['id'],
            defaults={
                'identifier_type_code': it['code'],
                'identifier_type_description': it['desc'],
                'status': 1,
                'created_by': 'system',
                'last_updated_by': 'system'
            }
        )
        id_type_objs[it['code']] = obj

    # 5. Create Party (The Insured Individual)
    amka_value = '12345678901'
    party_insured, created = Party.objects.get_or_create(
        party_id=1001,
        defaults={
            'client_id': client,
            'party_type': 'PERSON',
            'display_name': 'Ioannis Papadopoulos',
            'distinct_type': 'AMKA',
            'distinct_value': amka_value,
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 6. Create PartyRole for Insured
    role_insured, created = PartyRole.objects.get_or_create(
        party_id=party_insured,
        role_id=1001,
        defaults={
            'role_type_id': 1, # Linking to 'INS' role_type_id
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 7. Create PartyIdentifiers for Insured
    identifiers_insured = [
        {'id': 10001, 'type_id': 1, 'value': '1234567'},        # AMA
        {'id': 10002, 'type_id': 2, 'value': amka_value},      # AMKA
        {'id': 10003, 'type_id': 3, 'value': '987654321'},      # AFM
        {'id': 10004, 'type_id': 4, 'value': 'AN123456'},      # ADT
    ]

    for ident in identifiers_insured:
        PartyIdentifier.objects.get_or_create(
            identifier_id=ident['id'],
            defaults={
                'party_id': party_insured,
                'identifier_value': ident['value'],
                'identifier_type_id': ident['type_id'],
                'status': 1,
                'created_by': 'system',
                'last_updated_by': 'system'
            }
        )

    # 8. Create Person entry for the Insured
    Person.objects.get_or_create(
        person_id=1001,
        defaults={
            'party_id': party_insured,
            'first_name': 'Ioannis',
            'last_name': 'Papadopoulos',
            'date_of_birth': date(1985, 5, 15),
            'gender': 'M',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 9. Create Address for Insured
    Address.objects.get_or_create(
        address_id=1,
        defaults={
            'party_id': party_insured,
            'address_street': 'Acharnon',
            'address_number': '123',
            'city': 'Athens',
            'country': 'Greece',
            'postal_code': '10445',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 10. Create Party (The Employer)
    party_employer, created = Party.objects.get_or_create(
        party_id=2001,
        defaults={
            'client_id': client,
            'party_type': 'ORGANIZATION',
            'display_name': 'METLEN ENERGY & METALS S.A.',
            'distinct_type': 'AME',
            'distinct_value': '1234567890',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 11. Create Organization entry for the Employer
    Organization.objects.get_or_create(
        organization_id=2001,
        defaults={
            'party_id': party_employer,
            'name': 'METLEN ENERGY & METALS S.A.',
            'address': '8 Artemidos Str., Maroussi, Athens, 15125',
            'phone': '2101234567',
            'email': 'hr@metlen.gr',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 12. Create PartyRole for Employer
    role_employer, created = PartyRole.objects.get_or_create(
        party_id=party_employer,
        role_id=2001,
        defaults={
            'role_type_id': 2, # Linking to 'EMP' role_type_id
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 13. Create PartyIdentifiers for Employer
    identifiers_employer = [
        {'id': 20001, 'type_id': 5, 'value': '1234567890'},   # AME
        {'id': 20002, 'type_id': 3, 'value': '998877665'},   # AFM
    ]

    for ident in identifiers_employer:
        PartyIdentifier.objects.get_or_create(
            identifier_id=ident['id'],
            defaults={
                'party_id': party_employer,
                'identifier_value': ident['value'],
                'identifier_type_id': ident['type_id'],
                'status': 1,
                'created_by': 'system',
                'last_updated_by': 'system'
            }
        )

    # 14. Create Address for Employer
    Address.objects.get_or_create(
        address_id=2,
        defaults={
            'party_id': party_employer,
            'address_street': 'Artemidos',
            'address_number': '8',
            'city': 'Maroussi',
            'country': 'Greece',
            'postal_code': '15125',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 15. Create AccountTypes
    account_types = [
        {'id': 1, 'code': 'CONTRIB', 'desc': 'Current Contributions'},
        {'id': 2, 'code': 'DEBT_OVERDUE', 'desc': 'Overdue Debts'},
        {'id': 3, 'code': 'DEBT_SETTLED', 'desc': 'Settled Debts'},
    ]
    for at in account_types:
        AccountType.objects.get_or_create(
            account_type_id=at['id'],
            defaults={
                'account_type_code': at['code'],
                'account_type_description': at['desc'],
                'status': 1,
                'created_by': 'system',
                'last_updated_by': 'system'
            }
        )

    # 16. Create Account for Employer
    role_employer = PartyRole.objects.get(party_id=party_employer, role_type_id=2)
    account_employer, created = Account.objects.get_or_create(
        account_id=1,
        defaults={
            'party_role_id': role_employer,
            'account_type_id': 1, # Current Contributions
            'account_balance': 1250.50,
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 17. Create AccountTransactions (APD Debits)
    # Transaction 1: October 2025 (Paid)
    tx_oct, created = AccountTransaction.objects.get_or_create(
        account_transaction_id=2,
        defaults={
            'account_id': account_employer,
            'transaction_description': 'APD Submission - October 2025',
            'transaction_type': 'APD_SUBMISSION',
            'debit_credit_flag': 'D',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # Transaction 2: November 2025 (Unpaid)
    tx_nov, created = AccountTransaction.objects.get_or_create(
        account_transaction_id=1,
        defaults={
            'account_id': account_employer,
            'transaction_description': 'APD Submission - November 2025',
            'transaction_type': 'APD_SUBMISSION',
            'debit_credit_flag': 'D',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 18. Create TransactionObligations
    # Obligation 1: October (Paid)
    obl_oct, created = TransactionObligation.objects.update_or_create(
        obligation_id=2,
        defaults={
            'transaction_id': tx_oct,
            'obligation_description': 'Social Security Contribution - Oct 2025',
            'obligation_type': 'CONTRIBUTION',
            'month': 10,
            'reference_month': 10,
            'year': 2025,
            'rf_code': 'RF91023456789012345678910',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # Obligation 2: November (Unpaid)
    obl_nov, created = TransactionObligation.objects.update_or_create(
        obligation_id=1,
        defaults={
            'transaction_id': tx_nov,
            'obligation_description': 'Social Security Contribution - Nov 2025',
            'obligation_type': 'CONTRIBUTION',
            'month': 11,
            'reference_month': 11,
            'year': 2025,
            'rf_code': 'RF91123456789012345678911',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 19. Create ObligationBalances
    # Balance for October: 0 (Paid)
    ObligationBalance.objects.get_or_create(
        obligation_balance_id=2,
        defaults={
            'obligation_id': obl_oct,
            'amount': 452.40,
            'balance': 0.00,
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # Balance for November: 452.40 (Unpaid)
    ObligationBalance.objects.get_or_create(
        obligation_balance_id=1,
        defaults={
            'obligation_id': obl_nov,
            'amount': 452.40,
            'balance': 452.40,
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 20. Create InsuranceContribution for Insured Person (Linked to Nov obligation)
    InsuranceContribution.objects.get_or_create(
        insurance_contribution_id=1,
        defaults={
            'account_transaction_id': tx_nov,
            'obligation_id': obl_nov,
            'party_id': party_insured,
            'coverage_package_id': 101,
            'insurance_days': 25,
            'start_date': datetime(2025, 11, 1),
            'end_date': datetime(2025, 11, 30),
            'earning_type_id': 1,
            'gross_earnings': 1500.00,
            'total_contribution': 452.40,
            'employer_id': 2001,
            'insurance_id': 1001,
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 21. Create PartyRelationshipType
    rel_type, created = PartyRelationshipType.objects.update_or_create(
        relationship_type_id=1,
        defaults={
            'relationship_type_code': 'EMPLOYMENT',
            'relationship_type_description': 'Employer-Employee Relationship',
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    # 22. Create PartyRelationship between Employer role and Insured role
    # Convention: relation_from = Employer, relation_to = Insured
    PartyRelationship.objects.update_or_create(
        relationship_id=1,
        defaults={
            'party_id': party_insured, # Linking to the insured's party as the primary owner of this relationship record
            'relationship_type_id': 1,
            'relation_from': role_employer,
            'relation_to': role_insured,
            'active_date_from': date(2020, 1, 1),
            'active_date_to': date(2099, 12, 31),
            'status': 1,
            'created_by': 'system',
            'last_updated_by': 'system'
        }
    )

    print("Database seeded successfully with Party Relationship data!")

if __name__ == '__main__':
    seed()
