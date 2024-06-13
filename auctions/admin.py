from django.contrib import admin
from .models import Listing, Bid, Comment

# Register your models here.
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = [
        'owner', 
        'image_path',

        'title',
        'category',
        'description',
        
        'starting_bid',
        'minimum_buyout',
        'current_offer',
        'highest_bidder',
        
        'start_date',
        'end_date',
        
        'active',]

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = [
        'bidder',
        'listing',
        'date',
        'amount'
    ]

    @admin.register(Comment)
    class CommentAdmin(admin.ModelAdmin):
        list_display = [
            'user',
            'listing',
            'date',
            'title',
            'body'
        ]