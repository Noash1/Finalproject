from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Estate)
admin.site.register(ForSaleEstate)
admin.site.register(OnAuctionEstate)
admin.site.register(Bid)
admin.site.register(Comment)
