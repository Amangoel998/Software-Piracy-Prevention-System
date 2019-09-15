from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    '''Provides home page'''
    return render(request, 'utilities/home.html')

def loggedIn(request):
    '''Check if logged in'''
    if request.method == 'POST':
        uname = request.POST['username']
        return render(request, 'utilities/logn.html')
    else:
        return HttpResponse('<h1><b>Not Authorized</b></h1>')

def contact(request):
    '''Contact Page'''
    return render(request, 'utilities/Contactus.html')

def buy(request):
    '''Buy Page'''
    return render(request, 'utilities/Buy.html')

def about(request):
    '''About Page'''
    return render(request, 'utilities/Aboutus.html')

def download(request):
    '''Download Page'''
    return render(request, 'utilities/Download.html')

def notFound(request):
    '''Default Page When no other found'''
    return HttpResponse('<h1><b>NOT FOUND</b></h1>')