from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions

from piracy_prevention_api import models
from django.contrib.auth import authenticate

from datetime import date, timedelta, datetime




class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=20, required=True, label='First Name',)
    last_name = forms.CharField(max_length=20, required=True, label='Last Name')
    email = forms.EmailField(max_length=25, required=True, label='Email address')
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput, label='Password')

    def save(self, commit=True):
        try:
            if self.is_valid():
                user = models.UserProfile.objects.create_user(
                        email = self.cleaned_data['email'],
                        name = self.cleaned_data['first_name']+self.cleaned_data['last_name'],
                        password = self.cleaned_data['password'],
                    )
                return (user, 'Success')
            else:
                return (None, '')
        except Exception as error:
            return (None, 'User Already exist, Try Login')

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
        try:
            user = authenticate(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
            )
            return user
        except:
            return None

class BuyForm(forms.Form):
    email = forms.EmailField(max_length=25, required=True, label='Verify Email')
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
            return "You have already purchased"
        except:
            return "Something Invalid"
        if user2==user:
            if activation==None:
                try:
                    activation = models.ActivationList.objects.create(
                    user = user,
                    software = models.SoftwareProfile.objects.get(pk=1),
                    authorized_machine = self.cleaned_data['hardware_id'],
                    expiration_date = int(self.cleaned_data['validity_days']),
                )
                except:
                    return "The Hardware Id is Invalid"
                activation.expiration_date = date.today()+timedelta(days=int(self.cleaned_data['validity_days']))
                activation.save()
                return "Success"
            elif activation.is_activated:
                return "You have already Purchased"
            
        elif activation:
            return "You already Purchased the Software"
        else:
            return "Invalid: User Email doesn't Match"

class PaymentForm(forms.Form):
    holder_name = forms.CharField(max_length=20, required=True,)
    card_number = forms.IntegerField(required=True,max_value=10**12)
    expiry_month = forms.IntegerField(
        max_value=12,
        min_value=1,
        required=True,
        )
    expiry_year = forms.IntegerField(
        max_value=2030,
        min_value=2019,
        required=True,
        )

    cvv = forms.IntegerField(required=True, max_value=999, min_value=100, label='CVV', widget=forms.PasswordInput,)

    def start_activation(self,user):
        try:
            activation = models.ActivationList.objects.get(
                user=user
            )
        except exceptions.MultipleObjectsReturned:
            activation = models.ActivationList.objects.filter(
                user=user
            ).first()
        return ('Success', activation.activation_hash, )

class DownloadForm(forms.Form):
    email = forms.EmailField(max_length=25, required=True)
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput)
    address = forms.CharField(max_length=20, required=False)
    
    def check_user(self):
        user = authenticate(
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password']
        )
        if user:
            return True
        else:
            return False


class ContactForm(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=25, required=True)
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    
    def sendMessage(self):
        if not self.is_valid():
            return None
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        message = self.cleaned_data['message']
        return """
            Hi Admin,
            {0} contacted you and asked for the message:
            {1}
            If you want to reply, repply at {2}.
        """.format(name, message, email)

