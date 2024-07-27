from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import (
    TemplateView,
    ListView,
    FormView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import *
from realestate.utils import convert_currency
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required


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
        for_sale_estates = ForSaleEstate.objects.all()
        for_auction_estates = OnAuctionEstate.objects.all()
        if "type" in self.request.GET:
            """Getting a list of estate objects based on url parameter (i.e. property type in this case)"""
            estate_type = self.request.GET['type']
            for_sale_estates = for_sale_estates.filter(estate__type=estate_type)
            for_auction_estates = for_auction_estates.filter(estate__type=estate_type)
        context['for_sale'] = for_sale_estates.order_by('estate__name')
        context['on_auction'] = for_auction_estates.order_by('estate__name')
        return context


class EstateDetailView(DetailView):
    model = Estate
    template_name = 'estate_detail.html'
    context_object_name = 'estate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estate = self.get_object()
        context['comments'] = self.object.comments.all()
        last_sale = estate.forsaleestate_set.last()
        context['last_sale_price'] = last_sale.price if last_sale else -1
        last_bid_sum = -2
        last_auction = estate.onauctionestate_set.last()
        if last_auction:
            last_bid = last_auction.bid_set.last()
            last_bid_sum = last_bid.bidding_sum if last_bid else -1
        context['last_bid_sum'] = last_bid_sum
        return context

    def post(self, request, *args, **kwargs):
        estate = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.estate = estate
            comment.save()
            return redirect('estate_detail', pk=estate.id)
        context = self.get_context_data(estate=estate)
        context['comment_form'] = comment_form
        return self.render_to_response(context)


@login_required(login_url='login')
def estate_make_bid(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("estate_detail", args=[pk]))
    estate = get_object_or_404(Estate, pk=pk)
    last_auction = estate.onauctionestate_set.last()
    bid_sum = request.POST.get('bid_sum', 0)
    bid_sum = float(bid_sum)
    last_bid = last_auction.bid_set.last()
    # Need to check last_bid, there is no last bid.
    if last_bid and bid_sum > last_bid.bidding_sum:
        bid = Bid(estate=last_auction, bidding_sum=bid_sum, user=request.user)
        bid.save()
    return HttpResponseRedirect(reverse("estate_detail", args=[pk]))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_profile_page'] = True
        return context

    def get_user_profile(request, username):
        user = User.objects.get(username=username)
        return render(request, 'registration/profile.html', {"user": user})


class Profile(TemplateView):
    template_name = "registration/profile.html"


class About(TemplateView):
    template_name = "about.html"


class MyEstatesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Estate
    template_name = 'my_estates.html'
    context_object_name = 'estate'
    ordering = ['name']
    permission_required = 'my_estates'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['for_sale'] = ForSaleEstate.objects.all().order_by('estate__name')
        context['on_auction'] = OnAuctionEstate.objects.all().order_by('estate__name')
        return context



@login_required(login_url='login')
def add_estate_for_sale_view(request):
    if request.method == 'POST':
        estate_form = AddEstateForm(request.POST, request.FILES)
        estate_for_sale = AddEstateForSaleForm(request.POST)

        if estate_form.is_valid() and estate_for_sale.is_valid():
            estate = estate_form.save(commit=False)
            estate.user = request.user
            estate.category = 'sell'
            estate.save()
            for image in request.FILES.getlist('images'):
                img = Image(images=image)
                img.user = request.user
                img.save()
                estate.images.add(img)
            for_sale = estate_for_sale.save(commit=False)
            for_sale.user = request.user
            for_sale.estate = estate
            for_sale.save()
            return redirect('my_estates')

    else:
        estate_form = AddEstateForm()
        estate_for_sale = AddEstateForSaleForm()
    return render(request, 'add_estate.html', {
        'estate_form': estate_form,
        'estate_for_sale': estate_for_sale
    })


@login_required(login_url='login')
def add_estate_on_auction_view(request):
    if request.method == 'POST':
        estate_form = AddEstateForm(request.POST, request.FILES)
        estate_on_auction = AddEstateOnAuctionForm(request.POST)

        if estate_form.is_valid() and estate_on_auction.is_valid():
            estate = estate_form.save(commit=False)
            estate.user = request.user
            estate.category = 'auction'
            estate.save()
            for image in request.FILES.getlist('images'):
                img = Image(images=image)
                img.user = estate.user
                img.save()
                estate.images.add(img)
            on_auction = estate_on_auction.save(commit=False)
            on_auction.user = estate.user
            on_auction.estate = estate
            on_auction.save()
            return redirect('my_estates')
    else:
        estate_form = AddEstateForm()
        estate_on_auction = AddEstateOnAuctionForm()
    return render(request, 'add_estate.html', {
        'estate_form': estate_form,
        'estate_on_auction': estate_on_auction
    })


class EstateForSaleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Estate
    form_class = AddEstateForm
    template_name = 'add_estate.html'
    success_url = reverse_lazy('my_estates')
    permission_required = 'estate_for_sale_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['estate_form'] = AddEstateForm(self.request.POST, self.request.FILES, instance=self.get_estate())
            context['estate_for_sale'] = AddEstateForSaleForm(self.request.POST, instance=self.get_for_sale_estate())
        else:
            context['estate_form'] = AddEstateForm(instance=self.get_estate())
            context['estate_for_sale'] = AddEstateForSaleForm(instance=self.get_for_sale_estate())
        return context

    def get_for_sale_estate(self):
        return get_object_or_404(ForSaleEstate, estate=self.object)

    def get_estate(self):
        # id = self.get_form_kwargs()
        # for img in estate.images:
        #     img.
        return get_object_or_404(Estate, id=self.object.id)

    def form_valid(self, form):
        context = self.get_context_data()
        estate = context['estate_form']
        estate_for_sale = context['estate_for_sale']
        if estate.is_valid() and estate_for_sale.is_valid():
            response = super().form_valid(form)
            estate.save()
            estate_for_sale.save()
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EstateOnAuctionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Estate
    form_class = AddEstateForm
    template_name = 'add_estate.html'
    success_url = reverse_lazy('my_estates')
    permission_required = 'estate_on_auction_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['estate_form'] = AddEstateForm(self.request.POST, self.request.FILES, instance=self.get_estate())
            context['estate_on_auction'] = AddEstateOnAuctionForm(self.request.POST, instance=self.get_on_auction_estate())
        else:
            context['estate_form'] = AddEstateForm(instance=self.get_estate())
            context['estate_on_auction'] = AddEstateOnAuctionForm(instance=self.get_on_auction_estate())
        return context

    def get_on_auction_estate(self):
        return get_object_or_404(OnAuctionEstate, estate=self.object)

    def get_estate(self):
        # id = self.get_form_kwargs()
        # for img in estate.images:
        #     img.
        return get_object_or_404(Estate, id=self.object.id)

    def form_valid(self, form):
        context = self.get_context_data()
        estate = context['estate_form']
        estate_on_auction = context['estate_on_auction']
        if estate.is_valid() and estate_on_auction.is_valid():
            response = super().form_valid(form)
            estate.save()
            estate_on_auction.save()
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))


# Class for deleting estates
class EstateDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Estate
    template_name = 'estate_confirm_delete.html'
    success_url = reverse_lazy('my_estates')
    permission_required = 'estate_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estate = self.get_object()
        context['estate'] = estate
        return context


# Function for currency converter
def convert_currency_view(request):
    in_amount = request.GET['in_amount']
    in_amount = float(in_amount)
    in_currency = "EUR"
    out_currency = "USD"
    data = {'out_amount': convert_currency(in_amount, in_currency=in_currency, out_currency=out_currency), "out_currency": out_currency, "in_currency": in_currency}
    return JsonResponse(data)
