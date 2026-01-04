import os
import csv
import django
import uuid
from datetime import date, datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registry_app.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    Client, Party, PartyRole, PartyRoleType, PartyIdentifier, PartyIdentifierType, 
    Person, Organization, Address, Account, AccountType, AccountBalance, 
    AccountTransaction, TransactionBalance, TransactionObligation, 
    ObligationBalance, InsuranceContribution, InsuranceContributionBalance, 
    PartyRelationship, PartyRelationshipType
)

def populate():
    print("Starting comprehensive database population...")

    # 0. Cleanup financial models to remove "old" contributions
    # -------------------------------------------------------------------------
    print("  - Cleaning up old financial records...")
    InsuranceContributionBalance.objects.all().delete()
    InsuranceContribution.objects.all().delete()
    ObligationBalance.objects.all().delete()
    TransactionObligation.objects.all().delete()
    TransactionBalance.objects.all().delete()
    AccountTransaction.objects.all().delete()
    AccountBalance.objects.all().delete()
    Account.objects.all().delete()

    # 1. Create Users
    # -------------------------------------------------------------------------
    def create_user(username, email, password):
        user, created = User.objects.get_or_create(username=username, email=email)
        if created:
            user.set_password(password)
            user.save()
            print(f"  - Created user: {username}")
        return user

    user_insured = create_user('insured_user', 'insured@example.com', 'password123')
    user_insured_2 = create_user('insured_user_2', 'insured2@example.com', 'password123')
    user_employer = create_user('employer_user', 'employer@example.com', 'password123')

    # 2. Create Clients
    # -------------------------------------------------------------------------
    client_insured, _ = Client.objects.update_or_create(
        client_id=1,
        defaults={
            'user': user_insured,
            'name': 'Ioannis Papadopoulos',
            'address': 'Acharnon 123, Athens',
            'phone': '6900000000',
            'email': 'ioannis@example.com',
            'insurance_id': 'INS-001'
        }
    )
    
    client_employer, _ = Client.objects.update_or_create(
        client_id=2,
        defaults={
            'user': user_employer,
            'name': 'METLEN ENERGY & METALS S.A.',
            'address': 'Artemidos 8, Maroussi',
            'phone': '2101234567',
            'email': 'hr@metlen.gr',
            'insurance_id': 'EMP-2001'
        }
    )
    client_insured_2, _ = Client.objects.update_or_create(
        client_id=3,
        defaults={
            'user': user_insured_2,
            'name': 'Maria Papadopoulou',
            'address': 'Kifisias 55, Maroussi',
            'phone': '6911111111',
            'email': 'maria@example.com',
            'insurance_id': 'INS-002'
        }
    )
    print("  - Clients initialized.")

    # 3. Static Data (Role Types, ID Types, Account Types, Relationship Types)
    # -------------------------------------------------------------------------
    role_types = [
        (1, 'INS', 'Insured Person'),
        (2, 'EMP', 'Employer'),
    ]
    for rid, code, desc in role_types:
        PartyRoleType.objects.get_or_create(role_type_id=rid, defaults={'role_type_code': code, 'role_type_description': desc, 'created_by': 'sys'})

    id_types = [
        (1, 'AMA', 'AMA'), (2, 'AMKA', 'AMKA'), (3, 'AFM', 'AFM'), (4, 'ADT', 'ADT'), (5, 'AME', 'AME')
    ]
    for tid, code, desc in id_types:
        PartyIdentifierType.objects.get_or_create(identifier_type_id=tid, defaults={'identifier_type_code': code, 'identifier_type_description': desc, 'created_by': 'sys'})

    acc_types = [
        (1, 'CONTRIB', 'Current Contributions'),
        (2, 'SET_DEBT_OVERDUE', 'Settled Overdue Debts'),
        (3, 'UNSET_DEBT_OVERDUE', 'Unsettled Overdue Debts'),
    ]
    for aid, code, desc in acc_types:
        AccountType.objects.update_or_create(account_type_id=aid, defaults={'account_type_code': code, 'account_type_description': desc, 'created_by': 'sys'})

    PartyRelationshipType.objects.get_or_create(relationship_type_id=1, defaults={'relationship_type_code': 'EMPLOYMENT', 'relationship_type_description': 'Employer-Employee', 'created_by': 'sys'})
    print("  - Static types initialized.")

    # 4. Parties and Roles
    # -------------------------------------------------------------------------
    party_insured, _ = Party.objects.update_or_create(
        party_id=1001,
        defaults={'client_id': client_insured, 'party_type': 'PERSON', 'display_name': 'Ioannis Papadopoulos', 'distinct_type': 'AMKA', 'distinct_value': '12345678901', 'created_by': 'sys'}
    )
    role_insured, _ = PartyRole.objects.update_or_create(role_id=1001, defaults={'party_id': party_insured, 'role_type_id': 1, 'created_by': 'sys'})
    Person.objects.update_or_create(person_id=1001, defaults={'party_id': party_insured, 'first_name': 'Ioannis', 'last_name': 'Papadopoulos', 'created_by': 'sys'})

    party_insured_2, _ = Party.objects.update_or_create(
        party_id=1002,
        defaults={'client_id': client_insured_2, 'party_type': 'PERSON', 'display_name': 'Maria Papadopoulou', 'distinct_type': 'AMKA', 'distinct_value': '12345678902', 'created_by': 'sys'}
    )
    role_insured_2, _ = PartyRole.objects.update_or_create(role_id=1002, defaults={'party_id': party_insured_2, 'role_type_id': 1, 'created_by': 'sys'})
    Person.objects.update_or_create(person_id=1002, defaults={'party_id': party_insured_2, 'first_name': 'Maria', 'last_name': 'Papadopoulou', 'created_by': 'sys'})

    party_employer, _ = Party.objects.update_or_create(
        party_id=2001,
        defaults={'client_id': client_employer, 'party_type': 'ORGANIZATION', 'display_name': 'METLEN ENERGY & METALS S.A.', 'distinct_type': 'AME', 'distinct_value': '1234567890', 'created_by': 'sys'}
    )
    role_employer, _ = PartyRole.objects.update_or_create(role_id=2001, defaults={'party_id': party_employer, 'role_type_id': 2, 'created_by': 'sys'})
    Organization.objects.update_or_create(organization_id=2001, defaults={'party_id': party_employer, 'name': 'METLEN ENERGY & METALS S.A.', 'created_by': 'sys'})
    
    # 4b. Party Identifiers
    # -------------------------------------------------------------------------
    # Insured AMKA (type 2)
    PartyIdentifier.objects.update_or_create(
        identifier_id=1,
        defaults={'party_id': party_insured, 'identifier_value': '12345678901', 'identifier_type_id': 2, 'created_by': 'sys'}
    )
    # Employer AFM (type 3)
    PartyIdentifier.objects.update_or_create(
        identifier_id=2,
        defaults={'party_id': party_employer, 'identifier_value': '998877665', 'identifier_type_id': 3, 'created_by': 'sys'}
    )
    # Employer AME (type 5)
    PartyIdentifier.objects.update_or_create(
        identifier_id=3,
        defaults={'party_id': party_employer, 'identifier_value': '1234567890', 'identifier_type_id': 5, 'created_by': 'sys'}
    )

    # Employer AFM (type 3)
    PartyIdentifier.objects.update_or_create(
        identifier_id=4,
        defaults={'party_id': party_employer, 'identifier_value': '998877666', 'identifier_type_id': 3, 'created_by': 'sys'}
    )

    # Insured AMA (type 1)
    PartyIdentifier.objects.update_or_create(
        identifier_id=5,
        defaults={'party_id': party_insured, 'identifier_value': '1234567999', 'identifier_type_id': 1, 'created_by': 'sys'}
    )

    # Insured ADT (type 4)
    PartyIdentifier.objects.update_or_create(
        identifier_id=6,
        defaults={'party_id': party_insured, 'identifier_value': 'AO123456789', 'identifier_type_id': 4, 'created_by': 'sys'}
    )

    # Insured 2 AMKA (type 2)
    PartyIdentifier.objects.update_or_create(
        identifier_id=7,
        defaults={'party_id': party_insured_2, 'identifier_value': '12345678902', 'identifier_type_id': 2, 'created_by': 'sys'}
    )

    # Insured AMA (type 1)
    PartyIdentifier.objects.update_or_create(
        identifier_id=11,
        defaults={'party_id': party_insured_2, 'identifier_value': '1234567919', 'identifier_type_id': 1, 'created_by': 'sys'}
    )

    # Insured ADT (type 4)
    PartyIdentifier.objects.update_or_create(
        identifier_id=12,
        defaults={'party_id': party_insured_2, 'identifier_value': 'AO123456781', 'identifier_type_id': 4, 'created_by': 'sys'}
    )



    
    print("  - Parties, Roles, and Identifiers initialized.")

    # 5. Relationship
    # -------------------------------------------------------------------------
    PartyRelationship.objects.update_or_create(
        relationship_id=1,
        defaults={
            'party_id': party_insured,
            'relationship_type_id': 1,
            'relation_from': role_employer,
            'relation_to': role_insured,
            'active_date_from': date(2023, 11, 1),
            'active_date_to': date(2099, 12, 31),
            'created_by': 'sys'
        }
    )

    PartyRelationship.objects.update_or_create(
        relationship_id=2,
        defaults={
            'party_id': party_insured_2,
            'relationship_type_id': 1,
            'relation_from': role_employer,
            'relation_to': role_insured_2,
            'active_date_from': date(2023, 11, 1),
            'active_date_to': date(2099, 12, 31),
            'created_by': 'sys'
        }
    )

    # 6. Financial Data: Accounts and Balances
    # -------------------------------------------------------------------------
    # Retrieve AccountType instances
    type_contrib = AccountType.objects.get(account_type_id=1)
    type_settled = AccountType.objects.get(account_type_id=2)
    type_unsettled = AccountType.objects.get(account_type_id=3)

    # Account 1: Current Contributions
    acc_current, _ = Account.objects.get_or_create(
        account_id=1,
        defaults={'party_role_id': role_insured, 'account_type_id': type_contrib, 'account_balance': 0.00, 'created_by': 'sys'}
    )
    acc_insured_2, _ = Account.objects.get_or_create(
        account_id=4,
        defaults={'party_role_id': role_insured_2, 'account_type_id': type_contrib, 'account_balance': 0.00, 'created_by': 'sys'}
    )
    
    # Account 2: Settled Overdue (KEAO)
    # Total will be updated later based on installments
    acc_settled, _ = Account.objects.get_or_create(
        account_id=2,
        defaults={'party_role_id': role_employer, 'account_type_id': type_settled, 'account_balance': 0.00, 'created_by': 'sys'}
    )

    # Account 3: Unsettled Overdue (KEAO)
    acc_unsettled, _ = Account.objects.get_or_create(
        account_id=3,
        defaults={'party_role_id': role_employer, 'account_type_id': type_unsettled, 'account_balance': 153.50, 'created_by': 'sys'}
    )
    AccountBalance.objects.update_or_create(
        account_balance_id=3,
        defaults={'account_id': acc_unsettled, 'balance': 153.50, 'created_by': 'sys'}
    )

    # 7. Seed Insurance Contributions from CSV
    # -------------------------------------------------------------------------
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'insurance_contributions.csv')
    
    def seed_contributions(account_obj, party_obj, multiplier, id_offset):
        print(f"  - Seeding contributions for {party_obj.display_name} (Multiplier: {multiplier}x)...")
        total_acc_balance = 0
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                # Apply offset to IDs to ensure uniqueness across users
                tx_id = idx + 10 + id_offset
                obl_id = idx + 10 + id_offset
                ic_id = idx + 10 + id_offset
                
                # Parse dates
                start_parts = row['start_date'].split('/')
                end_parts = row['end_date'].split('/')
                start_date = date(int(start_parts[2]), int(start_parts[1]), int(start_parts[0]))
                end_date = date(int(end_parts[2]), int(end_parts[1]), int(end_parts[0]))
                
                month = start_date.month
                year = start_date.year
                
                # Parse numeric values and apply multiplier
                gross_earnings = float(row['gross_earnings']) * multiplier
                total_contribution = float(row['total_contribution']) * multiplier
                days = int(row['days']) if row['days'] else 0
                months = int(row['months']) if row['months'] else 0
                earnings_type = int(row['earnings_type'])
                branch_code = int(row['branch_code'])
                
                # Determine if paid (before Dec 2025)
                # For demo, keeping the same paid logic
                is_paid = start_date < date(2025, 11, 1)
                balance = 0.00 if is_paid else total_contribution
                
                # Transaction
                tx, _ = AccountTransaction.objects.update_or_create(
                    account_transaction_id=tx_id,
                    defaults={
                        'account_id': account_obj, 
                        'transaction_description': f'APD Submission {month:02d}/{year}', 
                        'transaction_type': 'APD', 
                        'debit_credit_flag': 'D', 
                        'created_by': 'sys'
                    }
                )
                TransactionBalance.objects.update_or_create(
                    transaction_balance_id=tx_id,
                    defaults={'transaction_id': tx, 'amount': total_contribution, 'balance': balance, 'created_by': 'sys'}
                )
        
                # Obligation
                # Generate unique RF code per user/contribution
                rf_suffix = f"{id_offset + idx:05d}"
                obl, _ = TransactionObligation.objects.update_or_create(
                    obligation_id=obl_id,
                    defaults={
                        'transaction_id': tx, 
                        'obligation_description': f'Contribution {month:02d}/{year}', 
                        'obligation_type': 'CONTRIB', 
                        'month': month, 
                        'reference_month': month, 
                        'year': year, 
                        'rf_code': f'RF91{year}{month:02d}00{rf_suffix}', 
                        'created_by': 'sys'
                    }
                )
                ObligationBalance.objects.update_or_create(
                    obligation_balance_id=obl_id,
                    defaults={'obligation_id': obl, 'amount': total_contribution, 'balance': balance, 'created_by': 'sys'}
                )
        
                # Insurance Contribution
                ic, _ = InsuranceContribution.objects.update_or_create(
                    insurance_contribution_id=ic_id,
                    defaults={
                        'account_transaction_id': tx, 
                        'obligation_id': obl, 
                        'party_id': party_obj, 
                        'coverage_package_id': branch_code, 
                        'insurance_days': days, 
                        'start_date': start_date, 
                        'end_date': end_date,
                        'earning_type_id': earnings_type,
                        'gross_earnings': gross_earnings,
                        'total_contribution': total_contribution,
                        'employer_id': 2001,
                        'insurance_id': 1001,
                        'created_by': 'sys'
                    }
                )
                InsuranceContributionBalance.objects.update_or_create(
                    insurance_contribution_balance_id=ic_id,
                    defaults={'insurance_contribution_id': ic, 'amount': total_contribution, 'balance': balance, 'created_by': 'sys'}
                )
                
                total_acc_balance += balance
        
        # Update account balance
        account_obj.account_balance = total_acc_balance
        account_obj.save()
        AccountBalance.objects.update_or_create(
            account_balance_id=account_obj.account_id,
            defaults={'account_id': account_obj, 'balance': total_acc_balance, 'created_by': 'sys'}
        )

    # Seed for Insured 1 (Account 1, Offset 0, Multiplier 1.0)
    seed_contributions(acc_current, party_insured, 1.0, 0)
    
    # Seed for Insured 2 (Account 4, Offset 1000, Multiplier 2.0)
    seed_contributions(acc_insured_2, party_insured_2, 2.0, 1000)
    

    # Seed representative records for KEAO (Accounts 2 and 3)
    # -------------------------------------------------------------------------
    # Account 2: Settled KEAO Enrichment (6 Monthly Installments)
    total_settled_bal = 0
    installment_amount = 75.13
    for inst in range(1, 7):
        tx_id = 300 + inst
        obl_id = 300 + inst
        month = inst
        year = 2024
        
        tx_settled, _ = AccountTransaction.objects.get_or_create(
            account_transaction_id=tx_id,
            defaults={
                'account_id': acc_settled, 
                'transaction_description': f'Settlement Installment {inst}/6', 
                'transaction_type': 'KEAO', 
                'debit_credit_flag': 'D', 
                'created_by': 'sys'
            }
        )
        TransactionBalance.objects.update_or_create(
            transaction_balance_id=tx_id, 
            defaults={'transaction_id': tx_settled, 'amount': installment_amount, 'balance': installment_amount, 'created_by': 'sys'}
        )
        
        obl_settled, _ = TransactionObligation.objects.get_or_create(
            obligation_id=obl_id, 
            defaults={
                'transaction_id': tx_settled, 
                'obligation_description': f'Installment {inst} (Settlement Plan)', 
                'obligation_type': 'SETTLED_DEBT', 
                'month': month, 
                'reference_month': month, 
                'year': year, 
                'rf_code': f'RF912024{month:02d}99999999',
                'created_by': 'sys'
            }
        )
        ObligationBalance.objects.update_or_create(
            obligation_balance_id=obl_id, 
            defaults={'obligation_id': obl_settled, 'amount': installment_amount, 'balance': installment_amount, 'created_by': 'sys'}
        )
        total_settled_bal += installment_amount

    # Update Account 2 balance
    acc_settled.account_balance = total_settled_bal
    acc_settled.save()
    AccountBalance.objects.update_or_create(
        account_balance_id=2,
        defaults={'account_id': acc_settled, 'balance': total_settled_bal, 'created_by': 'sys'}
    )

    # Unsettled KEAO Transaction/Obligation
    tx_unset, _ = AccountTransaction.objects.get_or_create(
        account_transaction_id=31,
        defaults={'account_id': acc_unsettled, 'transaction_description': 'KEAO Unsettled Debt 2023', 'transaction_type': 'KEAO', 'debit_credit_flag': 'D', 'created_by': 'sys'}
    )
    TransactionBalance.objects.update_or_create(transaction_balance_id=31, defaults={'transaction_id': tx_unset, 'amount': 153.50, 'balance': 153.50, 'created_by': 'sys'})
    obl_unset, _ = TransactionObligation.objects.get_or_create(obligation_id=31, defaults={'transaction_id': tx_unset, 'obligation_description': 'KEAO Natural Charges', 'obligation_type': 'KEAO_DEBT', 'month': 6, 'reference_month': 6, 'year': 2023, 'created_by': 'sys'})
    ObligationBalance.objects.update_or_create(obligation_balance_id=31, defaults={'obligation_id': obl_unset, 'amount': 153.50, 'balance': 153.50, 'created_by': 'sys'})

    print("\nDatabase successfully populated with comprehensive scenario!")
    print("Credentials:")
    print("  - Insured: insured_user / password123")
    print("  - Employer: employer_user / password123")

if __name__ == "__main__":
    populate()
