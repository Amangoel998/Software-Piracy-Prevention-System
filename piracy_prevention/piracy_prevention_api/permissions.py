from rest_framework import permissions


class DisableOptionsPermission(permissions.BasePermission):
    """
    Global permission to disallow all requests for method OPTIONS.
    """

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return False
        return True

class UpdateOwnProfile(permissions.BasePermission):
    """Allow a User to update its own profile"""

    # Add has_object_permission function to class
    # This is called when request is made to API
    def has_object_permission(self, request, view, obj):
        """Check is user edit their own profile"""

        # We check if method being made for request is Safe
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Now we check if user updating profile matches their own
        return obj.id == request.user.id


class UpdateOwnFeed(permissions.BasePermission):
    """Allow user only to update its own feed"""
    def has_object_permission(self, request, view, obj):
        """Check if user is updating its own feed"""
        if request.method == permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id == request.user.id


class CreateSoftware(permissions.BasePermission):
    """Admin can only create software profiles"""
    pass

class CreateActivation(permissions.BasePermission):
    """Application can only Activate softwares"""
    pass

class ViewActivation(permissions.BasePermission):
    """Only Admin can view Activations"""
    pass
