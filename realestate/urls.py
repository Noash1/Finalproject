from django.urls import path, include
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('estates/<int:pk>/', EstateDetailView.as_view(), name="estate_detail"),
    path('estates/<int:pk>/make-bid/', estate_make_bid, name="estate_make_bid"),
    path('registration/profile/', Profile.as_view(), name="profile"),
    path('about/', About.as_view(), name="about"),
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('my_estates/', MyEstatesView.as_view(), name='my_estates'),
    path('my_estates/add_for_sale', add_estate_for_sale_view, name='add_estate_for_sale'),
    path('my_estates/add_on_auction', add_estate_on_auction_view, name='add_estate_on_auction'),
    # Include the default auth urls after your custom definitions
    path('', include('django.contrib.auth.urls')),
]
