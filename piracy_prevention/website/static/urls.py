from django.conf.urls import url, include
from django.contrib import admin
from . import views

from django.conf import settings
from django.conf.urls.static import static

# When goto api/ request is passed to django app
# Which then lookup url pattern that first matches
# Then it pass all matches api urls to sub-urls in api
urlpatterns = [
    url(r'home', views.home),
    url(r'Buy', views.buy),
    url(r'Contact', views.contact),
    url(r'About', views.about),
    url(r'Download', views.download),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print('---------------------------'+str(settings.STATIC_URL)+str(settings.STATIC_ROOT))