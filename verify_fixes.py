
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registry_app.settings')
django.setup()

from core.models import InsuranceContribution, PartyRelationship, PartyRole, Party

def verify_updates():
    print("--- Verifying CSV Data Correction ---")
    # check a row that was previously wrong, e.g. Start Date 01/12/2023, Type 03
    # In CSV: 01/12/2023,31/12/2023,,,03,103,267.54,80.69,0470193611
    
    # Get Insured 1 (Party 1001)
    try:
        p1 = Party.objects.get(party_id=1001)
    except Party.DoesNotExist:
        print("FAIL: Party 1001 not found.")
        return

    ic = InsuranceContribution.objects.filter(
        party_id=p1,
        start_date=date(2023, 12, 1),
        earning_type_id=3
    ).first()
    
    if ic:
        print(f"Found Contribution (Type 03):")
        print(f"  - Earning Type: {ic.earning_type_id} (Expected: 3)")
        print(f"  - Package/Branch: {ic.coverage_package_id} (Expected: 103)")
        print(f"  - Total Contribution: {ic.total_contribution} (Expected: 80.69)")
        print(f"  - Days: {ic.insurance_days} (Expected: 0)")
        
        if ic.earning_type_id == 3 and ic.coverage_package_id == 103 and ic.insurance_days == 0:
             print("PASS: Bonus row data is correct.")
        else:
             print("FAIL: Bonus row data is incorrect.")
    else:
        print("FAIL: Could not find the specific contribution record.")

    print("\n--- Verifying Hire Date Fix ---")
    # Check PartyRelationship for Party 1001
    rel = PartyRelationship.objects.filter(party_id=p1, relationship_type_id=1).first()
    if rel:
        print(f"Relationship Active From: {rel.active_date_from}")
        if rel.active_date_from == date(2023, 11, 1):
            print("PASS: Hire date is 2023-11-01.")
        else:
            print(f"FAIL: Hire date is {rel.active_date_from}, expected 2023-11-01.")
    else:
        print("FAIL: Relationship not found.")

if __name__ == "__main__":
    verify_updates()
