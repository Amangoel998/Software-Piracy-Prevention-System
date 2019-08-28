#  To use this Custom model goto ../piracy_prevention/settings.py
# At last add AUTH_SER_MODEL = 'piracy_prevention_api.UserProfile'

from django.db import models
from django.contrib.auth.models import AbstractBaseUser #\for custom user model
from django.contrib.auth.models import PermissionsMixin #/
from django.contrib.auth.models import BaseUserManager  # for custom model manager
from django.conf import settings

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
    
class ProfileFeedItem(models.Model):
    """Profile Status Update"""
    # Add user profile field as foreign key for profile item
    user_profile = models.ForeignKey(
        # Can reference name of UserProfile class as string but we have to manually update all keys
        # When referencing auth user model, it's best to retrive from setting.py
        settings.AUTH_USER_MODEL,
        # On delete argument tells what to do if remote field is deleted
        # So it cascade changes in related fields ie remove feed if user is removed
        # Other option is to set it None and set feed item as None
        on_delete = models.CASCADE,
    )
    # Status text contain feed update
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        """Return model as String"""
        return self.status_text