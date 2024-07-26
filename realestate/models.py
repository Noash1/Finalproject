from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Model Image that handles multiple images.
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/')


# Model Estate has all the needed fields to describe the estate, that owner wants to put to auction or just sell
class Estate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=[('sell', 'Sell'), ('auction', 'Auction')],
                                help_text='For sale or on auction')
    type = models.CharField(choices=[('apartment', 'Apartment'),
                                     ('villa', 'Villa'),
                                     ('townhouse', 'Townhouse'),
                                     ('mansion', 'Mansion'),
                                     ('duplex', 'Duplex'),
                                     ('castle', 'Castle'),
                                     ('other', 'Other')
                                     ],
                            default='other',
                            help_text='Estate type')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(null=True, help_text='Description of the property')
    rooms = models.PositiveIntegerField(default=1, help_text='Rooms in total')
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(default=0, help_text='Size of the house in square meters')
    architectural_style = models.CharField(
        choices=[('contemporary', 'Contemporary'),
                 ('mid-century modern', 'Mid-century Modern'),
                 ('classical revival', 'Classical Revival'),
                 ('tudor', 'Tudor'),
                 ('georgian', 'Georgian'),
                 ('victorian', 'Victorian'),
                 ('gothic revival', 'Gothic Revival'),
                 ('mediterranean', 'Mediterranean'),
                 ('shingle', 'Shingle'),
                 ('italianate', 'Italianate'),
                 ('spanish colonial', 'Spanish Colonial'),
                 ('ranch', 'Ranch'),
                 ('other', 'Other')
                 ],
        default='other',
        help_text='Style of the house'
    )
    added_date = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(Image)  # To upload images
    video = models.FileField(
        upload_to='videos/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])],
        help_text='optional'
    )  # validators are to make users to upload only specific filetypes

    def __str__(self):
        return self.name

    def get_full_description(self):
        return (f"{self.user.username} {self.category} {self.name} {self.description} {self.rooms} {self.bedrooms}"
                f"{self.bathrooms} {self.size} {self.architectural_style} {self.added_date}")


# model for estates that are for selling
class ForSaleEstate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estate} {self.price} {self.user.username} {self.start_date}"


# model for estates that are going for auction
class OnAuctionEstate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    starting_price = models.PositiveIntegerField()
    asking_price = models.PositiveIntegerField()
    sold_for = models.PositiveIntegerField(null=True, blank=True)
    starting_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.estate} {self.user.username} {self.starting_price} {self.starting_date} {self.end_date}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(OnAuctionEstate, on_delete=models.CASCADE)
    bidding_sum = models.PositiveIntegerField(default=1000)
    bidding_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estate.estate.name} {self.bidding_date} {self.bidding_sum} {self.user.username}"


# comment model for giving comments or asking questions about estates
class Comment(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content}"
