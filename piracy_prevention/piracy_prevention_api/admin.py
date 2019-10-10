#!/usr/bin/python3
from django.contrib import admin
from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.SoftwareProfile)
admin.site.register(models.ActivationList)
