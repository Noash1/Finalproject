from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Model Category where we give two options 'Sell' that has key 'S' and 'Auction', that has key 'A'.
class Category(models.Model):
    CATEGORY_FIELD = {
        "S": "Sell",
        "A": "Auction"
    }
    category = models.CharField(max_length=1, choices=CATEGORY_FIELD, default="S")

    def __str__(self):
        return self.category


# Model Estate has all the needed fields to describe the estate, that owner wants to put to auction or just sell
class Estate(models.Model):
    id = models.AutoField(primary_key=True)  # Gives ID for every estate
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    rooms = models.PositiveIntegerField(default=1)  # Positive integer field so no one could put negative number
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(default=0)
    architectural_style = models.CharField(max_length=255, null=True, blank=True, default='Other')
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)  # To upload images.!!AFTER WE NEED TO REMOVE blank==True
    video = models.FileField(
        upload_to='videos/',
        blank=True,  # !!AFTER WE NEED TO REMOVE blank==True
        validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]
    )  # validators are to make users to upload only specific filetypes
    floor_plans = models.ImageField(blank=True)  # images for floor plans


# model for estates that are for selling
class ForSaleEstate(models.Model):
    id = models.AutoField(primary_key=True)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)


# model for estates that are going for auction
class OnAuctionEstate(models.Model):
    id = models.AutoField(primary_key=True)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    starting_price = models.PositiveIntegerField(default=0)
    asking_price = models.PositiveIntegerField(default=0, null=True, blank=True)
    bidding_step = models.PositiveIntegerField(default=1000)
    current_price = models.PositiveIntegerField(default=starting_price)
    bidding_price = models.PositiveIntegerField(default=current_price)
    end_date = models.DateTimeField(auto_now_add=True)


# don't know how to make those models???????
"""
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate_id = models.ForeignKey(OnAuctionEstate, on_delete=models.CASCADE)
    estate_name = models.ForeignKey(OnAuctionEstate, on_delete=models.CASCADE)
    bidding_sum = models.ForeignKey(OnAuctionEstate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.estate_name} - {self.bidding_sum} - {self.user}"


class AuctionResults(models.Model):
    estate = models.ForeignKey(OnAuctionEstate, on_delete=models.CASCADE)
    sold_for = models.ForeignKey(OnAuctionEstate, on_delete=models.CASCADE)
"""

# comment model for giving comments or asking questions about estates
class Comments(models.Model):
    comment = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.content}"
