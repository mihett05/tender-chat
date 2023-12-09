from django.db import models
from django.contrib.auth.models import AbstractUser as _User


class UserTypes(models.TextChoices):
    CUSTOMER = 'customer'
    CONTRACTOR = 'contractor'


class User(_User):
    image = models.ImageField("image", blank=True, null=True, upload_to='images/')
    email = models.EmailField("email address", unique=True, null=False, blank=False)
    company = models.CharField("company name", unique=True, editable=False)
    user_type = models.CharField(choices=UserTypes.choices, editable=False)

    REQUIRED_FIELDS = ('email', 'password', 'company', 'user_type')

    class Meta:
        pass
