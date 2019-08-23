#!/usr/bin/python3
from django.contrib import admin
from piracy_prevention_api import models

admin.site.register(models.UserProfile)