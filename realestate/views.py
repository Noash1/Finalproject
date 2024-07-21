from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


class SignUpForm(UserCreationForm):
        email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.'
    )


class CustomLogoutView(LogoutView):

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm

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


class Signup(TemplateView):
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_login_page'] = True  # Add this line
        return context


#class Login(TemplateView):
    #template_name = "registration/login.html"

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context['is_signup_page'] = True  # Add this line
        #return context
