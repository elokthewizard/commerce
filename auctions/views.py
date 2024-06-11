from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from decimal import Decimal

from .models import User, Listing

def add_favorite(request, pk):
    favorited = get_object_or_404(Listing, pk=pk)
    if request.user not in favorited.favorite.all():
        favorited.favorite.add(request.user)
    return redirect('index')

def remove_favorite(request, pk):
    favorited = get_object_or_404(Listing, pk=pk)
    if request.user in favorited.favorite.all():
        favorited.favorite.remove(request.user)
    return redirect('index')

def favorite(request):
    favorites = Listing.objects.all()
    context = {'favorites': favorites}

# create use model form ot hold form data
class ListingForm(forms.ModelForm):
    # inherit model members as form fields
    class Meta:
        model = Listing
        fields = '__all__'

        # change default widget start and end date
        widgets = {
            'start_date': forms.HiddenInput(),
            'end_date': forms.SelectDateWidget()
        }

        exclude = [
            'owner',
            'current_offer'
        ]

class ListingDetailView(DetailView):
    model = Listing


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# handle new lisitng
def create_listing(request):
    if request.method == "POST":
    
        form = ListingForm(request.POST, instance=Listing())
        
        if request.user is not None and form.is_valid():
            
            # save form data in listing instance but dont commit yet
            new_listing = form.save(commit=False)
            # set value of owner field to current user
            new_listing.owner = request.user
            
            print("Starting bid:", request.POST['starting_bid'])
            print("Minimum buyout:", request.POST['minimum_buyout'])

            new_listing.starting_bid = Decimal(int(request.POST['starting_bid']))
            new_listing.minimum_buyout = Decimal(int(request.POST['minimum_buyout']))

            new_listing.save()

        listings = Listing.objects.all()
        print(form.errors)
        return render(request, "auctions/index.html", {
            "listings": listings
        })
    
    
    else:
        form = ListingForm(instance=Listing())
        return render(request, "auctions/create-listing.html", {
            "form": form
        })
    