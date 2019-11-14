from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions

from piracy_prevention_api import models
from django.contrib.auth import authenticate

import datetime

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=20, required=True, label='First Name',)
    last_name = forms.CharField(max_length=20, required=True, label='Last Name')
    email = forms.EmailField(max_length=25, required=True, label='Email address')
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput, label='Password')

    def save(self, commit=True):
        user = models.UserProfile.objects.create_user(
                email = self.cleaned_data['email'],
                name = self.cleaned_data['first_name']+self.cleaned_data['last_name'],
                password = self.cleaned_data['password'],
            )
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=25, required=True, label='Email address')
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput, label='Password')
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            raise forms.ValidationError("Must have these fields")
    
    def get_user(self):
        user = authenticate(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        return user

class BuyForm(forms.Form):
    full_name = forms.CharField(max_length=20, required=False, label='Full Name',)
    email = forms.EmailField(max_length=25, required=True, label='Verify Email address')
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput, label='Verify Password')
    hardware_id = forms.CharField(max_length=40, required=True, label='Hardware ID',)
    address = forms.CharField(max_length=20, required=False, label='Address',)
    
    CHOICES= [
    (365, '1 Year'),
    (180,'6 Months'),
    (90, '3 Months'),
    ]
    validity_days= forms.IntegerField(label='Activation Period', widget=forms.Select(choices=CHOICES))

    def create_activation(self, user):
        try:
            user2 = authenticate(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                )
        except:
            return "Invalid: User Does not Exist"
        try:
            activation = models.ActivationList.objects.get(authorized_machine=self.cleaned_data['hardware_id'])
        except exceptions.ObjectDoesNotExist:
            activation = None
        except exceptions.MultipleObjectsReturned:
            return "You already purchased"
        except:
            return "Something Invalid"
        if user2==user:
            try:
                activation = models.ActivationList.objects.create(
                    user = user,
                    software = models.SoftwareProfile.objects.get(pk=1),
                    authorized_machine = self.cleaned_data['hardware_id'],
                    expiration_date = int(self.cleaned_data['validity_days']),
                )
                return "Success"
            except:
                return "The Hardware Id is Invalid"
        elif activation:
            return "You already Purchased the Software"
        else:
            return "Invalid: User Email doesn't Match"

class PaymentForm(forms.Form):
    holder_name = forms.CharField(max_length=20, required=True, label="Card Holder's Name",)
    card_number = forms.IntegerField(
        required=True,
        label='Card Number',
        )
    expiry_month = forms.IntegerField(
        max_value=12,
        min_value=1,
        required=True,
        label='Expiry Month',
        widget=forms.TextInput(attrs={'placeholder': 'MM'})
        )
    expiry_year = forms.IntegerField(
        max_value=2030,
        min_value=2019,
        required=True,
        label='Expiry Year',
        widget=forms.TextInput(attrs={'placeholder': 'YYYY'})
        )
    cvv = forms.IntegerField(required=True, max_value=999, label='CVV', widget=forms.TextInput(attrs={'placeholder': 'XXX'}))

    def start_activation(self,user):
        try:
            activation = models.ActivationList.objects.get(
                user=user
            )
        except exceptions.MultipleObjectsReturned:
            activation = models.ActivationList.objects.filter(
                user=user
            ).first()
        models.ActivationList.objects.filter(pk=activation.activation_hash).update(is_activated=True)
        return ('Success',activation.activation_hash)

class DownloadForm(forms.Form):
    full_name = forms.CharField(max_length=20, required=False, label='Full Name',)
    email = forms.EmailField(max_length=25, required=True, label='Verify Email address')
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput, label='Verify Password')
    address = forms.CharField(max_length=20, required=False, label='Address',)
    
    def check_user(self):
        user = authenticate(
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password']
        )
        if user:
            return True
        else:
            return False

# class RenewBookForm(forms.Form):
#     renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

#     def clean_renewal_date(self):
#         data = self.cleaned_data['renewal_date']
        
#         # Check if a date is not in the past. 
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))

#         # Check if a date is in the allowed range (+4 weeks from today).
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

#         # Remember to always return the cleaned data.
#         return data