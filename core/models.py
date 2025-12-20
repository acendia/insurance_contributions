# core/models.py
from django.db import models
# from django.contrib.auth.models import User
# import uuid

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

# class Client(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
#     client_id = models.IntegerField(unique=True)
#     name = models.CharField(max_length=100)
#     address = models.CharField(max_length=255)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField()
#     insurance_id = models.CharField(max_length=30, unique=True)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

# class Party(models.Model):
#     client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
#     party_id = models.IntegerField(unique=True)
#     party_type = models.CharField(max_length=30)
#     display_name = models.CharField(max_length=100)
#     distinct_type = models.CharField(max_length=30)
#     distinct_value = models.CharField(max_length=30)

#     status = models.CharField(max_length=1)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=30)
#     last_update_date = models.DateTimeField(auto_now=True)
#     last_updated_by = models.CharField(max_length=30)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

#     def __str__(self):
#         return f"{self.party_id} – {self.party_type}"

# class PartyRole(models.Model):
#     party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
#     role_id  = models.IntegerField(unique=True)
#     role_type_id = models.IntegerField(unique=True)

#     status = models.CharField(max_length=1)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=30)
#     last_update_date = models.DateTimeField(auto_now=True)
#     last_updated_by = models.CharField(max_length=30)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

# class PartyRoleType(models.Model):
#     role_type_id = models.IntegerField(unique=True)
#     role_type_code = models.CharField(max_length=30)
#     role_type_description = models.CharField(max_length=255)

#     status = models.CharField(max_length=1)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=30)
#     last_update_date = models.DateTimeField(auto_now=True)
#     last_updated_by = models.CharField(max_length=30)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

# class PartyIdentifier(models.Model):
#     party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
#     identifier_id = models.IntegerField(unique=True)
#     identifier_value = models.CharField(max_length=30)
#     identifier_type_id = models.IntegerField(unique=True)

#     status = models.CharField(max_length=1)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=30)
#     last_update_date = models.DateTimeField(auto_now=True)
#     last_updated_by = models.CharField(max_length=30)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

# class PartyIdentifierType(models.Model):
#     identifier_type_id = models.IntegerField(unique=True)
#     identifier_type_code = models.CharField(max_length=30)
#     identifier_type_description = models.CharField(max_length=255)

#     status = models.CharField(max_length=1)
#     creation_date = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=30)
#     last_update_date = models.DateTimeField(auto_now=True)
#     last_updated_by = models.CharField(max_length=30)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    


