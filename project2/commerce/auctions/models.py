from django.contrib.auth.models import AbstractUser
from django.db import models

#Remember that each time you change anything in auctions/models.py, 
# you’ll need to first run python manage.py makemigrations 
# and then python manage.py migrate to migrate those changes to your database.
class User(AbstractUser):
    pass

class Categories(models.Model): #Um pra muitos
    name = models.CharField(max_length=24)

    def __str__(self):
        return f"Category: {self.name}"

class Listings(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_user")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="listings_category")
    status = models.BooleanField(default=True)
    image_url = models.CharField(max_length=2083)

    def __str__(self):
        return f"{self.id}: Title: {self.title} Description: {self.description} First Bid: {self.starting_bid} Category: {self.category} Status: {self.status}"


class Bids(models.Model): #=Lances
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    value = models.DecimalField(max_digits=8, decimal_places=2)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_id")
    
    
    def __str__(self):
        return f"User: {self.user} Value:{self.value} Listing:{self.listing}"

class Comments(models.Model): #=Comments made on listings
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comment_listing")
    comment = models.CharField(max_length=255)
    
    def __str__(self):
        return f"User: {self.user} Listing: {self.listing} Comment: {self.comment}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlist_listing")

    def __str__(self):
        return f"User: {self.user} Listing: {self.listing}"