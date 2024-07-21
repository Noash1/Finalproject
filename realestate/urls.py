from django.urls import path, include
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('forsale/', ForSaleView.as_view(), name="for_sale"),
    path('auction/', AuctionView.as_view(), name="for_auction"),
    path('registration/profile/', Profile.as_view(), name="profile"),
    path('about/', About.as_view(), name="about"),
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
path('accounts/profile/', ProfileView.as_view(), name='profile'),

    # Include the default auth urls after your custom definitions
    path('', include('django.contrib.auth.urls')),
]