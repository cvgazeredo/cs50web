from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Categories, Bids, Comments, Watchlist


def index(request):
    if request.user.is_authenticated:
        active_Listings = Listings.objects.all()

        for item in active_Listings:
            currentPrice = Bids.objects.filter(listing=item).values_list('value', flat=True).order_by('-value')[0]
            item.currentPrice = currentPrice
        
        return render(request, "auctions/index.html", {
                "listings": active_Listings,
            })
    return render (request, "auctions/index.html")


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

@login_required
def create(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        starting_bid = request.POST["starting_bid"]

        create_Listing = Listings(
            user=user,
            title=title,
            description=description,
            image_url = image_url,
            category=Categories.objects.get(name=category),
            starting_bid=starting_bid,
            status=True
        )
        
        create_Listing.save()

        #Insert starting bid in Bids db 
        listing_id_db = Listings.objects.filter(title=title).values_list('id', flat=True).order_by('id')
        listing_id = listing_id_db.get()

        starting_bid_on_bids = Bids(
            listing=Listings.objects.get(id=listing_id), 
            value=starting_bid, 
            user=user
        )
        starting_bid_on_bids.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        categories = Categories.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })


def listing(request, listing_id):
    user = request.user
    listing = Listings.objects.get(id=listing_id)
    user_watchlist = Watchlist.objects.filter(user=user, listing=listing)

    if user_watchlist:
        print("Item in user's Watchlist")
        isInUserWatchList = True
    else:
        print("Item NOT in user's Watchlist")
        isInUserWatchList = False

    bids = Bids.objects.filter(listing=listing_id).values_list('value', flat=True).order_by('-value').values('value')[0]
    bid = bids.get('value')

    user_of_listing_db = Listings.objects.filter(id=listing_id).values_list('user', flat=True).values('user')[0]
    user_of_listing = user_of_listing_db.get('user')


    user_of_page_db = User.objects.filter(username=user).values_list('id', flat=True).values('id')[0]

    user_of_page = user_of_page_db.get('id')


    if user_of_listing == user_of_page:
        isUserOfListing = True
        print(isUserOfListing)
    else:
        isUserOfListing = False

    winner_user = bids = Bids.objects.filter(listing=listing_id).values_list('value', flat=True).order_by('-value').values('user')[0]
    winner = winner_user.get('user')
    
    if user_of_page == winner:
        WinnerUser = True
    else:
        WinnerUser = False
   

    comments = Comments.objects.filter(listing=listing_id).values('comment')
  

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "isInUserWatchList": isInUserWatchList,
        "bids": bid,
        "isUserOfListing": isUserOfListing,
        "comments": comments,
        "WinnerUser": WinnerUser
        })

def close_auction(request, listing_id):
    user = request.user
    listing = Listings.objects.all()

    close_auction = Listings.objects.filter(id=listing_id).update(status='False')

    return HttpResponse("You remove your listing from the auction")

@login_required
def watchlist(request): #to display users watchlist
    user = request.user
    watchlists = Watchlist.objects.filter(user=User.objects.get(username=user))

    return render(request, "auctions/watchlist.html", {
        "watchlists": watchlists
        })

def categories(request):
    categories = Categories.objects.all()
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category_id):
    listings = Listings.objects.filter(category=Categories.objects.get(id=category_id))
    print(listings)

    return render(request, "auctions/categories_listings.html", {
        "listings": listings
    })

@login_required
def add_to_watchlist(request, listing_id):
    user = request.user
    listing = Listings.objects.get(id=listing_id)

    watchlist = Watchlist(
            user=User.objects.get(username=user),
            listing=Listings.objects.get(id=listing_id)
        )

    watchlist.save()
   
    return HttpResponse("Added to your Watchlist!")

def remove_watchlist(request, listing_id):
    user = request.user
    listing = Listings.objects.get(id=listing_id)


    delete_item = Watchlist.objects.get(user=user,
            listing=listing
        )

    delete_item.delete()
   
    return HttpResponse("Removed from your Watchlist!")

def place_bid(request, listing_id):
    if request.method == 'POST':
        #Get user 
        user = request.user

        #Check bid made by the user
        bid = float(request.POST["bid"])
        print(f"Bid made by the user was: {bid}")
        
        #Check if bid made by current user is greater than last bid
        greater_bid_db = Bids.objects.filter(listing=listing_id).values_list('value', flat=True).order_by('-value').values('value')[0]
        print(f"Thats the greater bid made in the listing: {greater_bid_db}")
        greater_bid = greater_bid_db.get('value')
        print(greater_bid)


        if bid <= greater_bid:
            print("Bid must be greater than current price!")
            return HttpResponse("Your bid must be greater than the current price!") 
        else:
            print("Bid is greater than all bids")
            new_bid = Bids(listing=Listings.objects.get(id=listing_id), 
            value=bid, 
            user=user
            )
            print(new_bid)
            new_bid.save() 
            
        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
            

    else:
        return render(request, "auctions/listing.html", { 
            "listing_starting_bid": listing_starting_bid,
            "listing_bids": listing_bids
        })

@login_required
def comment(request, listing_id):
    if request.method == 'POST':
        #Get user 
        user = request.user

        #Get user's comment
        comment = request.POST["comment"]
        if not comment:
            return HttpResponse("You must write a comment")
        print(f"Comment made by the user was: {comment}")

        #Save user's comment
        save_comment = Comments(listing=Listings.objects.get(id=listing_id), 
            comment=comment, 
            user=user
            )
        print(save_comment)
        save_comment.save() 

        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
    
    else: 
        return render(request, "auctions/listing.html") 
        



