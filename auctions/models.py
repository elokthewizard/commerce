from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

def default_end_date():
    return timezone.now() + timedelta(days=3)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=256)

    start_date = models.DateTimeField(auto_now_add=True, blank=False)
    end_date = models.DateTimeField(default=default_end_date)

    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_offer = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title