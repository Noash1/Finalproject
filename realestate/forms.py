from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .views import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Estate, ForSaleEstate, OnAuctionEstate, Comment
from django.contrib.auth.models import User


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
        help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return super().clean_password2()


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class AddEstateForm(forms.ModelForm):
    images = MultipleFileField(label='Pictures')

    class Meta:
        model = Estate
        widgets = {'description': forms.Textarea(attrs={'rows': 3}),
                   'images': forms.CheckboxSelectMultiple}
        exclude = ['user', 'category']


class AddEstateForSaleForm(forms.ModelForm):
    class Meta:
        model = ForSaleEstate
        exclude = ['user', 'estate']


class AddEstateOnAuctionForm(forms.ModelForm):
    class Meta:
        model = OnAuctionEstate
        widgets = {'end_date': forms.NumberInput(attrs={'type': 'date'})}
        exclude = ['user', 'estate', 'sold_for']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {'content': forms.Textarea(attrs={'rows': 4})}
        fields = ['content']
        labels = {'content': ''}
