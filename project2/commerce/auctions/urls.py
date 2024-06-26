from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("listing/remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("listing/close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_listings, name="category_listings")

    
]
