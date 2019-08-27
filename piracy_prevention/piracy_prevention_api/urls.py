from django.conf.urls import url, include
from piracy_prevention_api import views

from rest_framework import routers

router = routers.DefaultRouter()

# Register specific viewsets with some the user
# Arg is name of URL we want ,the viewset to register and base name for viewset
# Base name will be used to retrieve urls from router
router.register('first-viewset', views.FirstViewSet, base_name = 'first-viewset')

# We do not type basename coz we have queryset object in the view
# Django figure out the name itself
router.register('profiles', views.UserProfileViewSet)

# When goto api/ request is passed to django app
# Which then lookup url pattern that first matches
# Then it pass all matches api urls to sub-urls in api
urlpatterns = [
    url(r'^first-apiview/',views.FirstApiView.as_view()),
    url(r'^login/',views.UserLoginApiView.as_view()),
    # 'Blank' Coz we dont want to add prefix instead all urls in base of this url
    # This also create additional API Root directory page
    url(r'^', include(router.urls))
]