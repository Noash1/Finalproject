from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView
from django.shortcuts import render, redirect
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


class EstateCreateView(CreateView):
    model = Estate
    template_name = 'estate_create.html'
    fields = '__all__'
    # success_url = reverse_lazy('index')


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



