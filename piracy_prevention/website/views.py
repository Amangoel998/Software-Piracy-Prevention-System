from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View

from django.contrib.auth import authenticate, login, logout
# from .forms import SignUpForm
from .forms import *

def loggingin(request):
    '''Login Page'''
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
                return redirect('/home')
            elif not user:
                message = 'Invalid User'
    else:
        form = LoginForm()
    return render(request, 'login.html',{
        'form':form,
        'page_name':'Login',
        'nstate_value':'Signup',
        'nstate_url':'/Signup',
        'message' : message,
        })
def signup(request):
    '''Signup Page'''
    message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # messages.success(request, 'Account Successfully Created')
            login(request, user, backend = 'piracy_prevention_api.backends.MyAuthBackend')
            return redirect('/home')
        else:
            message = "Incorrect"
    else:
        form = SignUpForm()
    return render(request, 'signup.html',{
        'form':form,
        'page_name':'Signup',
        'nstate_value':'Login',
        'nstate_url':'/Login',
        'message' : message,
        })

def payment(request):
    '''Payment Page'''
    if not request.user.is_authenticated:
        return render(request, 'payment.html',{
        'message': "You Need to Authenticate to access",
        'page_name':'Payment Portal',
        'nstate_value':'Login',
        'nstate_url':'/Login'
        })
    message = ''
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            message, activation_id = form.start_activation(request.user, )
            if message == 'Success':
                return render(request, 'success.html',{
                    'activation_id':activation_id,
                    'message':message,
                    'page_name':'Successfully Activated',
                    'nstate_value':'Login',
                    'nstate_url':'/Login'
                    })
    else:
        form = PaymentForm()
    return render(request, 'payment.html',{
        'form':form,
        'message':message,
        'page_name':'Payment Portal',
        'nstate_value':'Login',
        'nstate_url':'/Login'
        })

def buy(request):
    '''Buy Page'''
    if not request.user.is_authenticated:
        return render(request, 'buy.html',{
        'message': "You Need to Authenticate to access",
        'page_name':'Buy Now',
        'nstate_value':'Login',
        'nstate_url':'/Login'
        })
    message = ''
    if request.method == 'POST':
        form = BuyForm(request.POST)
        if form.is_valid():
            message = form.create_activation(request.user)
            if message == 'Success':
                return redirect('/Payment')
    else:
        form = BuyForm()
    return render(request, 'buy.html',{
        'form':form,
        'message':message,
        'page_name':'But Now',
        'nstate_value':'Login',
        'nstate_url':'/Login'
        })
   
def loggingout(request):
    '''Logout Page'''
    logout(request)
    return redirect('/home')
     
def download(request):
    '''Download Page'''
    if not request.user.is_authenticated:
        return render(request, 'download.html',{
        'message': "You Need to Authenticate to access",
        'page_name':'Download Now',
        'nstate_value':'Login',
        'nstate_url':'/Login'
        })
    message = ''
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            if form.check_user():
                return redirect('/Buy')
            else:
                message = "Invalid User"
    else:
        form = DownloadForm()
    return render(request, 'download.html',{
        'form':form,
        'message':message,
        'page_name':'Download Now',
        'nstate_value':'Login',
        'nstate_url':'/Login'
        })

def home(request):
    '''Home page'''
    return render(request, 'home.html',{'page_name':'Home','nstate_value':'Login','nstate_url':'/Login'})

def contact(request):
    '''Contact Page'''
    return render(request, 'contact.html',{'page_name':'Contact us','nstate_value':'Login','nstate_url':'/Login'})

def about(request):
    '''About Page'''
    return render(request, 'about.html',{'page_name':'About us','nstate_value':'Login','nstate_url':'/Login'})

def notFound(request):
    '''Default Page When no other found'''
    return render(request, 'unathorized.html',{'page_name':'Unauthorized'})