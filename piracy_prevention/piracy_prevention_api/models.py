#  To use this Custom model goto ../piracy_prevention/settings.py
# At last add AUTH_SER_MODEL = 'piracy_prevention_api.UserProfile'

from django.db import models
from django.contrib.auth.models import AbstractBaseUser #\for custom user model
from django.contrib.auth.models import PermissionsMixin #/
from django.contrib.auth.models import BaseUserManager  # for custom model manager
from django.conf import settings
from django.utils.timezone import now

import jwt
import uuid
from .hashmaker import Key
from datetime import datetime, timedelta, date

# Classes should be separted by 2 linespace from up and bellow
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    # Function to manipulate objects within module

    # This create a user object
    def create_user(self, email, name, password = None):
        if not email:
            raise ValueError('User must have an email')
        
        # Normalize the email and make the object
        email = self.normalize_email(email)
        user = self.model(email = email, name = name)
        user.is_superuser = False
        user.is_staff = False
        user.is_activated = False
        # Django encrypt password using this method
        user.set_password(password)

        # Save the user for multiple database in future
        user.save(using = self._db)
        return user
    
    # Create Super user like SysAdmin
    def create_superuser(self, email, name, password):
        """Create Super User"""
        user = self.create_user(email, name, password)
        
        # This attribute is created by PermissionMixin automatically
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)

        return user


# Create your models here.
class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users"""
    # Now we create custom columns on UserProfile table
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255)
    is_activated = models.BooleanField(default=False)
    # Field for Permission System

    # To check if user profile is enabled or not 
    is_active = models.BooleanField(default = True)
    # To check if user is staff member and has access
    is_staff = models.BooleanField(default = False)

    # Model Manager to use custom model for Django CLI
    # It create and control User using Django CLI
    # Must be objects only
    objects = UserProfileManager()

    # Replace Userfield and other for custom manager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # Functions for Django to interact with custom model manager
    def get_full_name(self):
        """Retrieve Full Name"""
        return self.name
    def get_short_name(self):
        """Retrieve Short Name"""
        return self.name
    # String Reprentation of our model
    def __str__(self):
        """Retrieve String Representation"""
        return self.email
    
class SoftwareProfile(models.Model):
    """Software Item Product"""
    software_name = models.CharField(max_length=50,unique=True)
    software_organization = models.CharField(max_length=50)
    active_users = models.ManyToManyField(UserProfile, through = 'ActivationList')

    def __repr__(self):
        return self.software_name

class ActivationListManager(models.Manager):
    """Manage Activations"""

    def create(self, user, software, authorized_machine, expiration_date):
        activation_request = self.model(
            user = UserProfile.objects.get(email=user),
            software = SoftwareProfile.objects.get(pk=software),
            authorized_machine = authorized_machine,
            expiration_date = date.today() + timedelta(days=expiration_date),
        )
        activation_request.save(using = self._db)
        return activation_request
    def activate(self, activate=False, machine_code='aaa-bb'):
        self.model.objects.filter(authorized_machine=machine_code).update(field2='cool')

class ActivationList(models.Model):
    """Model for Activations"""
    software = models.ForeignKey(SoftwareProfile, on_delete=models.CASCADE)
    user = models.OneToOneField(UserProfile, on_delete = models.CASCADE)
    activation_date = models.DateField(auto_now_add = True, editable=False)
    expiration_date = models.DateField(auto_now_add = True, editable= True)
    authorized_machine = models.UUIDField(null=False, editable=False,unique=True)
    activation_hash = models.CharField(max_length=255,default = Key, primary_key = True)
    is_activated = models.BooleanField(default=False, )
    objects = ActivationListManager

    def __repr__(self):
        return self.user+" using "+self.software+" activated on "+self.activation_date