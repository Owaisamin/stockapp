from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.reusable_methods import generate_six_length_random_number
from stocks_project.settings import *
import uuid
from django.db.models import Q, UniqueConstraint
from utils.base_models import LogsMixin
from utils.reusable_methods import generate_access_token

# Create your models here.

class User(AbstractUser, LogsMixin):
    """Fully featured User model, email and password are required.
        Other fields are optional.
    """
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    def get_access_token(self):
        return generate_access_token(self)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Token(LogsMixin):
    """Token model for authentication"""

    user = models.ForeignKey(
        AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE
    )
    token = models.TextField(max_length=500)
    status = models.IntegerField(default=1)

class Company(LogsMixin):
    ticker = models.CharField(primary_key=True, max_length=10)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class StockPrice(LogsMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()
