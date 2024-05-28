from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_offer = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title