from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import *


class CustomLogoutView(LogoutView):

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm

    def from_valid(self, form):
        login(self.request, form.get_user())
        next_url = self.request.GET.get('next', 'profile')
        return redirect(next_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_login_page'] = True
        return context


def signup(request):
    form = SignUpForm(request.POST or None)  # Initialize form for GET and POST requests
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registration/signup.html', {'form': form, 'is_signup_page': True})


class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_login_page'] = True  # Add this line
        return context


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


class EstateDetailView(DetailView):
    model = Estate
    template_name = 'estate_detail.html'
    context_object_name = 'estate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estate = self.get_object()
        last_sale = estate.forsaleestate_set.last()
        context['last_sale_price'] = last_sale.price if last_sale else -1
        last_bid_sum = -2
        last_auction = estate.onauctionestate_set.last()
        if last_auction:
            last_bid = last_auction.bid_set.last()
            last_bid_sum = last_bid.bidding_sum if last_bid else -1
        context['last_bid_sum'] = last_bid_sum
        return context


def estate_make_bid(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("estate_detail", args=[pk]))
    estate = get_object_or_404(Estate, pk=pk)
    last_auction = estate.onauctionestate_set.last()
    bid_sum = request.POST.get('bid_sum', 0)
    bid_sum = float(bid_sum)
    last_bid = last_auction.bid_set.last()
    if last_bid and bid_sum > last_bid.bidding_sum:
        bid = Bid(estate=last_auction, bidding_sum=bid_sum, user=request.user)
        bid.save()
    return HttpResponseRedirect(reverse("estate_detail", args=[pk]))


class ProfileView(TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_profile_page'] = True
        return context

    def get_user_profile(request, username):
        user = User.objects.get(username=username)
        return render(request, 'registration/profile.html', {"user": user})


class ForSaleView(TemplateView):
    template_name = "forsale.html"


class AuctionView(TemplateView):
    template_name = "forauction.html"


class Profile(TemplateView):
    template_name = "registration/profile.html"


class About(TemplateView):
    template_name = "about.html"


def add_estate_view(request):
    estate_form = AddEstateForm
    estate_for_sale = AddEstateForSaleForm
    estate_on_auction = AddEstateOnAuctionForm

    if request.method == 'POST':
        estate_form = AddEstateForm(request.POST, prefix='estate_form')
        estate_for_sale = AddEstateForSaleForm(request.POST, prefix='estate_for_sale')
        estate_on_auction = AddEstateOnAuctionForm(request.POST, prefix='estate_on_auction')

        if estate_form.is_valid() and estate_for_sale.is_valid():
            estate = estate_form.save(commit=False)
            estate.user = request.user  # The logged-in user
            for_sale = estate_for_sale.save(commit=False)
            for_sale.user = estate.user
            for_sale.estate = estate
            estate.save()
            for_sale.save()
            return redirect('index.html')

        elif estate_form.is_valid() and estate_on_auction.is_valid():
            # Process estate and on_auction data
            pass
        else:
            estate_form = AddEstateForm(prefix='estate_form')
            estate_for_sale = AddEstateForSaleForm(prefix='estate_for_sale')
            estate_on_auction = AddEstateOnAuctionForm(prefix='estate_on_auction')

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
