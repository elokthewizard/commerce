from django.urls import path

from . import views
from .views import ListingDetailView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("register", views.register, name="register"),
    path("listing/<int:pk>/", ListingDetailView.as_view(), name='listing-detail'),
]
