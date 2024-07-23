from django import forms
from .models import Estate, ForSaleEstate, OnAuctionEstate
from django.contrib.auth.models import User


class AddEstateForm(forms.ModelForm):
    class Meta:
        model = Estate
        widgets = {'For sale or on auction': forms.RadioSelect,
                   'Description of the property': forms.Textarea(attrs={'rows': 3})}
        exclude = ['user']


class AddEstateForSaleForm(forms.ModelForm):
    class Meta:
        model = ForSaleEstate
        exclude = ['user', 'estate']


class AddEstateOnAuctionForm(forms.ModelForm):
    class Meta:
        model = OnAuctionEstate
        widgets = {'end_date': forms.NumberInput(attrs={'type': 'date'})}
        exclude = ['user', 'estate', 'sold_for']
