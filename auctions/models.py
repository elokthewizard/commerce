from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

# set default end date

def default_end_date():
    return timezone.now() + timedelta(days=3)

class Listing(models.Model):
    # setup one to many relationship to User class
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")

    # allow user to link image via url
    image_path = models.CharField(max_length=64)

    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    description = models.TextField(max_length=256)

    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_buyout = models.DecimalField(max_digits=10, decimal_places=2)
    current_offer = models.DecimalField(max_digits=10, decimal_places=2)
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="highest_bidder")

    start_date = models.DateTimeField(auto_now_add=True, blank=False)
    end_date = models.DateTimeField(default=default_end_date)

    active = models.BooleanField(default=True)

    favorite = models.ManyToManyField(User, related_name='user_favorite')

    def __str__(self):
        return self.title
    
    # if no offer has been made yet, default to starting bid (thanks copilot!)
    def save(self, *args, **kwargs):
        if not self.current_offer:
            self.current_offer = self.starting_bid
        super().save(*args, **kwargs)

    
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=32)
    comment = models.TextField(max_length=128)