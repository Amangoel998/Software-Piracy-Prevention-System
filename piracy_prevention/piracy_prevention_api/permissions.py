from rest_framework import permissions


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
        return obj.method == request.user.id