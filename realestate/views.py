from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import *

# Create your views here.


# generates first page that is loaded
class HomeView(ListView):
    model = Estate
    template_name = 'index.html'
    context_object_name = 'estate'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['for_sale'] = ForSaleEstate.objects.all().order_by('estate__name')
        context['on_auction'] = OnAuctionEstate.objects.all().order_by('estate__name')
        return context


class ForSaleView(TemplateView):
    template_name = "forsale.html"


class AuctionView(TemplateView):
    template_name = "forauction.html"


class Contact(TemplateView):
    template_name = "contact.html"


class About(TemplateView):
    template_name = "about.html"
