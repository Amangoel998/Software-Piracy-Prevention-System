from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    '''Home page'''
    return render(request, 'home.html',{'page_name':'Home','login_value':'Login'})

def login(request):
    '''Login Page'''
    return render(request, 'login.html',{'page_name':'Login','login_value':'Login'})

def contact(request):
    '''Contact Page'''
    return render(request, 'contact.html',{'page_name':'Contact us','login_value':'Aman'})

def buy(request):
    '''Buy Page'''
    return render(request, 'buy.html',{'page_name':'But Now!!','login_value':'Aman'})

def about(request):
    '''About Page'''
    return render(request, 'about.html',{'page_name':'About us','login_value':'Login'})

def download(request):
    '''Download Page'''
    return render(request, 'download.html',{'page_name':'Download','login_value':'Aman'})

def signup(request):
    '''Signup Page'''
    return render(request, 'signup.html',{'page_name':'Signup'})

def payment(request):
    '''Payment Page'''
    return render(request, 'payment.html',{'page_name':'Payment Portal'})

def notFound(request):
    '''Default Page When no other found'''
    return HttpResponse('<h1><b>NOT FOUND</b></h1>')