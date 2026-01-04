# core/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

# class UserProfile(models.Model):
#     """
#     One‑to‑One relationship with the built‑in User model.
#     Stores extra information that is not part of the core auth schema.
#     """
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     insurance_id = models.CharField(
#         max_length=30,
#         unique=True,
#         help_text="Unique identifier for the user's insurance record."
#     )

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    client_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    insurance_id = models.CharField(max_length=30, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

class Party(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    party_id = models.IntegerField(unique=True)
    party_type = models.CharField(max_length=30)
    display_name = models.CharField(max_length=100)
    distinct_type = models.CharField(max_length=30)
    distinct_value = models.CharField(max_length=30)

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.party_id} – {self.party_type}"

class PartyRole(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    role_id  = models.IntegerField(unique=True)
    role_type_id = models.IntegerField()

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class PartyRoleType(models.Model):
    role_type_id = models.IntegerField(unique=True)
    role_type_code = models.CharField(max_length=30)
    role_type_description = models.CharField(max_length=255)

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class PartyRelationship(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    relationship_id = models.IntegerField(unique=True)
    relationship_type_id = models.IntegerField()
    relation_from = models.ForeignKey(PartyRole, on_delete=models.CASCADE, related_name='relationships_from')
    relation_to = models.ForeignKey(PartyRole, on_delete=models.CASCADE, related_name='relationships_to')
    active_date_from = models.DateField()
    active_date_to = models.DateField()

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    


class PartyRelationshipType(models.Model):
    relationship_type_id = models.IntegerField(unique=True)
    relationship_type_code = models.CharField(max_length=30)
    relationship_type_description = models.CharField(max_length=255)

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    

class PartyIdentifier(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    identifier_id = models.IntegerField(unique=True)
    identifier_value = models.CharField(max_length=30)
    identifier_type_id = models.IntegerField()

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class PartyIdentifierType(models.Model):
    identifier_type_id = models.IntegerField(unique=True)
    identifier_type_code = models.CharField(max_length=30)
    identifier_type_description = models.CharField(max_length=255)

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    


class Person(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    person_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Organization(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    organization_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Address(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    address_id = models.IntegerField(unique=True)
    address_street = models.CharField(max_length=50)
    address_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

########################################
# Insurance Contribution Models
########################################

class AccountType(models.Model):
    account_type_id = models.IntegerField(unique=True)
    account_type_code = models.CharField(max_length=30)
    account_type_description = models.CharField(max_length=255)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Account(models.Model):
    account_id = models.IntegerField(unique=True)
    party_role_id = models.ForeignKey(PartyRole, on_delete=models.CASCADE, related_name='accounts')
    account_type_id = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name='accounts')
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class AccountBalance(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    account_balance_id = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class AccountTransaction(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    account_transaction_id = models.IntegerField(unique=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=30)
    debit_credit_flag = models.CharField(max_length=1)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class TransactionBalance(models.Model):
    transaction_id = models.ForeignKey(AccountTransaction, on_delete=models.CASCADE)
    transaction_balance_id = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    


class TransactionObligation(models.Model):
    transaction_id = models.ForeignKey(AccountTransaction, on_delete=models.CASCADE)
    obligation_id = models.IntegerField()
    obligation_description = models.CharField(max_length=255)
    obligation_type = models.CharField(max_length=30)
    month = models.IntegerField() # months > 12 (13: Easter Bonus, 14: Annual leave allowance/Vacation Bonus, 15: Christmas Bonus)
    reference_month = models.IntegerField() # months <= 12
    year = models.IntegerField()
    rf_code = models.CharField(max_length=30, blank=True, null=True)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class ObligationBalance(models.Model):
    obligation_id = models.ForeignKey(TransactionObligation, on_delete=models.CASCADE)
    obligation_balance_id = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)



class InsuranceContribution(models.Model):
    insurance_contribution_id = models.IntegerField(unique=True)
    account_transaction_id = models.ForeignKey(AccountTransaction, on_delete=models.CASCADE)
    obligation_id = models.ForeignKey(TransactionObligation, on_delete=models.CASCADE)
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='contributions')
    coverage_package_id = models.IntegerField()
    insurance_days = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    earning_type_id = models.IntegerField()
    gross_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    total_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    employer_id = models.IntegerField()
    insurance_id = models.IntegerField()

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class InsuranceContributionBalance(models.Model):
    insurance_contribution_id = models.ForeignKey(InsuranceContribution, on_delete=models.CASCADE)
    insurance_contribution_balance_id = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Payment(models.Model):
    payment_id = models.IntegerField(unique=True)
    account_transaction_id = models.ForeignKey(AccountTransaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    last_update_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.CharField(max_length=30)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)