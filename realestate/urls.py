from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('forsale/', ForSaleView.as_view(), name="for_sale"),
    path('auction/', AuctionView.as_view(), name="for_auction"),
]