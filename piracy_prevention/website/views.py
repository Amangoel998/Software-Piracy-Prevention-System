from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.base import View
import os
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.http import FileResponse
from .backends import sendActivationMail, sendContactMail

def payment(request):
    '''Payment Page'''
    message = ''
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            message, activation_id = payment_form.start_activation(request.user, )
            if message == 'Success':
                sendActivationMail(activation_id, request.user.email)
                return redirect('/home')
    else:
        payment_form = PaymentForm()
    return render(request, 'payment.html',{
        'payment_form':payment_form,
        'message':message,
        'page_name':'Payment Portal',
        })

def buy(request):
    '''Buy Page'''
    message = ''
    buy_form = BuyForm()
    signup_form = SignUpForm()
    login_form = LoginForm()
    if request.method == 'POST':
        if 'LoggingIn' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/Buy')
                else:
                    message = 'Invalid User'

        elif "SigningUp" in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user, message = signup_form.save()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/Buy')
            else:
                message = "Incorrect"

        elif "BuyingSoftware" in request.POST:
            buy_form = BuyForm(request.POST)
            if buy_form.is_valid():
                message = buy_form.create_activation(request.user)
                if message == 'Success':
                    return redirect('/Payment')
        else:
            message = 'Invalid Inputs'

    return render(request, 'buy.html',{
        'login_form': login_form,
        'signup_form': signup_form,
        'buy_form': buy_form,
        'message':message,
        'page_name':'Buy Now',
        })
   
def loggingout(request):
    '''Logout Page'''
    logout(request)
    return redirect('/home')
     
def download(request):
    '''Download Page'''
    message = ''
    if request.user.is_authenticated:
        download_form = DownloadForm()
        signup_form = None
        login_form = None
    else:
        download_form = None
        signup_form = SignUpForm()
        login_form = LoginForm()
    if request.method == 'POST':
        if 'LoggingIn' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/Download')
                else:
                    message = 'Invalid User'

        elif "SigningUp" in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user, message = signup_form.save()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/Download')
            else:
                message = "Incorrect"
                
        elif "DownloadingSoftware" in request.POST:
            download_form = DownloadForm(request.POST)
            if download_form.is_valid():
                if download_form.check_user():
                    strpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/static/example.exe'
                    return FileResponse(open(strpath,'rb'))
                else:
                    message="Invalid User"

    return render(request, 'download.html',{
        'login_form': login_form,
        'signup_form': signup_form,
        'download_form': download_form,
        'message': message,
        'page_name':'Download Software',
    })

def home(request):
    '''Home page'''
    message = ''
    signup_form = SignUpForm()
    login_form = LoginForm()
    if request.method == 'POST':
        if 'LoggingIn' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/home')
                else:
                    message = 'Invalid User'

        elif "SigningUp" in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user, message = signup_form.save()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/home')
            else:
                message = "Incorrect"
        

    return render(request, 'home.html',{
        'signup_form': signup_form,
        'login_form': login_form,
        'page_name':'Home',
        'message': message
    })

def contact(request):
    '''Contact Page'''
    message = ''
    signup_form = SignUpForm(request.POST or None)
    login_form = LoginForm(request.POST or None)
    contact_form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if 'LoggingIn' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/Contact')
                else:
                    message = 'Invalid User'

        elif "SigningUp" in request.POST:
            if signup_form.is_valid():
                user, message = signup_form.save()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/Contact')
            else:
                message = "Incorrect"
        
        elif "ContactingAdmin" in request.POST and contact_form.is_valid():
                sendContactMail(contact_form.sendMessage())
                return redirect('/home')
                
    return render(request, 'contact.html',{
        'signup_form': signup_form,
        'login_form': login_form,
        'contact_form': contact_form,
        'page_name':'Contact Us',
        'message': message
    })

def about(request):
    '''About Page'''
    message = ''
    signup_form = SignUpForm()
    login_form = LoginForm()
    if request.method == 'POST':
        if 'LoggingIn' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/About')
                else:
                    message = 'Invalid User'

        elif "SigningUp" in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user, message = signup_form.save()
                if user:
                    login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                    return redirect('/About')
            else:
                message = "Incorrect"
                
    return render(request, 'about.html',{
        'signup_form': signup_form,
        'login_form': login_form,
        'page_name':'About Our Product',
        'message': message
    })

def team(request):
    '''Team Page'''
    message = ''
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user, message = signup_form.save()
            login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
            return redirect('/Team')
        
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            if user:
                login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                return redirect('/Team')
            elif not user:
                message = 'Invalid User'
    else:
        signup_form = SignUpForm()
        login_form = LoginForm()
    return render(request, 'team.html',{
        'signup_form': signup_form,
        'login_form': login_form,
        'page_name':'Professional Team',
        'message': message
    })
