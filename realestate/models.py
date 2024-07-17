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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text='Enter the name of the property')
    description = models.TextField(null=True, help_text='Description of the property')
    rooms = models.PositiveIntegerField(default=1, help_text='How many rooms total')  # Positive integer field so no one could put negative number
    bedrooms = models.PositiveIntegerField(default=1, help_text='Number of bedrooms')
    bathrooms = models.PositiveIntegerField(default=1, help_text='Number of bathrooms')
    size = models.PositiveIntegerField(default=0, help_text='Size of the house in square meters')
    architectural_style = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default='Not specified',
        help_text='Add the style of the house'
    )
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)  # To upload images.!!AFTER WE NEED TO REMOVE blank==True
    video = models.FileField(
        upload_to='videos/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])],

        help_text='Video of the property (optional)'
    )  # validators are to make users to upload only specific filetypes
    floor_plans = models.ImageField(blank=True, help_text='Optional')  # images for floor plans

    def __str__(self):
        return (self.user.username,
                self.category,
                self.name,
                self.description,
                self.rooms,
                self.bedrooms,
                self.bathrooms,
                self.size,
                self.architectural_style,
                self.added_date,
                self.image,
                self.video,
                self.floor_plans)


# model for estates that are for selling
class ForSaleEstate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.estate,
                self.price,
                self.user.username,
                self.start_date)


# model for estates that are going for auction
class OnAuctionEstate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    starting_price = models.PositiveIntegerField(default=0)
    asking_price = models.PositiveIntegerField(default=0)
    sold_for = models.PositiveIntegerField()
    starting_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.estate,
                self.user.username,
                self.starting_price,
                self.starting_date,
                self.end_date)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(OnAuctionEstate, on_delete=models.CASCADE)
    bidding_sum = models.PositiveIntegerField(default=1000)
    bidding_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.estate.estate.name,
                self.bidding_date,
                self.bidding_sum,
                self.user.username)


# comment model for giving comments or asking questions about estates
class Comment(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content}"
