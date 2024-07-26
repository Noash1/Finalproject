from django.contrib import admin
from .models import *


class EstateAdmin(admin.ModelAdmin):
    column_names = ('id', 'name', 'category', 'architectural_style', 'added_date')
    list_display = column_names
    list_filter = column_names
    search_fields = column_names


# Register your models here.
# admin.site.register(Category)
admin.site.register(Estate, EstateAdmin)
admin.site.register(Image)
admin.site.register(ForSaleEstate)
admin.site.register(OnAuctionEstate)
admin.site.register(Bid)
admin.site.register(Comment)
