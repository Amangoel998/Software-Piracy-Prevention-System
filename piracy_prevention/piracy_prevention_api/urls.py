from django.conf.urls import url
from piracy_prevention_api import views

# When goto api/ request is passed to django app
# Which then lookup url pattern that first matches
# Then it pass all matches api urls to sub-urls in api
urlpatterns = [
    url(r'^first-api/',views.FirstAPI.as_view()),
]