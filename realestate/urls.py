from django.urls import path, include
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('forsale/', ForSaleView.as_view(), name="for_sale"),
    path('auction/', AuctionView.as_view(), name="for_auction"),
    path('contact/', Contact.as_view(), name="contact"),
    path('about/', About.as_view(), name="about"),
    path('my_estates/new', add_estate_view, name='add_estate'),
]
