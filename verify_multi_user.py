
import os
import django
from django.db.models import Sum

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registry_app.settings')
django.setup()

from core.models import InsuranceContribution, Party

def verify_contributions():
    p1 = Party.objects.get(party_id=1001)
    p2 = Party.objects.get(party_id=1002)

    c1_count = InsuranceContribution.objects.filter(party_id=p1).count()
    c2_count = InsuranceContribution.objects.filter(party_id=p2).count()
    
    c1_sum = InsuranceContribution.objects.filter(party_id=p1).aggregate(Sum('total_contribution'))['total_contribution__sum'] or 0
    c2_sum = InsuranceContribution.objects.filter(party_id=p2).aggregate(Sum('total_contribution'))['total_contribution__sum'] or 0

    print(f"User 1 ({p1.display_name}): {c1_count} contributions, Total: {c1_sum:.2f}")
    print(f"User 2 ({p2.display_name}): {c2_count} contributions, Total: {c2_sum:.2f}")

    if c1_count == c2_count and c1_count > 0:
        print("PASS: Contribution counts match.")
    else:
        print("FAIL: Contribution counts do not match or are zero.")

    if abs(c2_sum - (c1_sum * 2)) < 0.1:
        print("PASS: User 2 total is double User 1 total.")
    else:
        print(f"FAIL: User 2 total ({c2_sum}) is NOT double User 1 total ({c1_sum}).")

if __name__ == "__main__":
    verify_contributions()
