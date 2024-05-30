from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listings, Categories, Bids, Comments, Watchlist

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listings)
admin.site.register(Categories)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)
