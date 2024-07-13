from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


# generates first page that is loaded
class HomeView(TemplateView):
    template_name = "home.html"


class ForSaleView(TemplateView):
    template_name = "forsale.html"


class AuctionView(TemplateView):
    template_name = "forauction.html"
