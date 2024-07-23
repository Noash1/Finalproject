from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from .models import *
from .forms import AddEstateForm, AddEstateOnAuctionForm, AddEstateForSaleForm

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


# class CategoryView(ListView):
#     model = Category
#     template_name = 'add_estate.html'
#     context_object_name = 'category'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category'] = Category.objects.all()
#         return context


class ForSaleView(TemplateView):
    template_name = "forsale.html"


class AuctionView(TemplateView):
    template_name = "forauction.html"


class Contact(TemplateView):
    template_name = "contact.html"


class About(TemplateView):
    template_name = "about.html"


def add_estate_view(request):
    estate_form = AddEstateForm()
    estate_for_sale = AddEstateForSaleForm()
    estate_on_auction = AddEstateOnAuctionForm()

    if request.method == 'POST':
        estate_form = AddEstateForm(request.POST)
        estate_for_sale = AddEstateForSaleForm(request.POST)
        estate_on_auction = AddEstateOnAuctionForm(request.POST)

        if estate_form.is_valid() and estate_for_sale.is_valid():
            # Process estate and for_sale data
            pass
        elif estate_form.is_valid() and estate_on_auction.is_valid():
            # Process estate and on_auction data
            pass
        else:
            pass

    return render(request,
                  'add_estate.html',
                  {'estate_form': estate_form,
                   'estate_for_sale': estate_for_sale,
                   'estate_on_auction': estate_on_auction}
                  )

# def add_estate_view(request):
#     if request.method == 'POST':
#         form = AddEstateForm(request.POST)
#         if form.is_valid():
#             estate = form.save(commit=False)
#             estate.user = request.user  # The logged-in user
#             estate.save()
#             return redirect('index.html')
#     else:
#         form = AddEstateForm()
#     return render(request, 'add_estate.html', {'form': form})


# class AddEstateView(CreateView):
#     model = Estate
#     form_class = AddEstateForm
#     template_name = 'add_estate.html'
#     success_url = reverse_lazy('home')
#
#     def get_user(self, request):
#         if request.user.is_authenticated:
#             user = request.user
#             return user
