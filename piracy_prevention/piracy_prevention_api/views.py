from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers, models, permissions



# Any Request Made to View is assigned to this
class FirstApiView(APIView):
    """My First API View"""

    serializer_class = serializers.FirstSerializer

    # GET is used to retrive list of objects on every Request
    # Request arg is set by rest framework
    def get(self, request, format = None):
        apiview = [
            'Use methods as functions (GET, PUT, POST, PATCH, DELETE)',
            'Is similar to traditional API',
            'Gives most control over the Application logic',
            'Is mapped manually to URLs',
        ]
        # Return Response that convert dictionary/list to json
        return Response({'message' : 'Hello My First API', 'apiview' : apiview})
    
    # Create post function to post message with our Name
    def post(self,request):
        """Post our name"""
        
        # self.serializer_class comes with APIView
        # That retrieve configured serializer class for our view
        serializer = self.serializer_class(data = request.data)

        # Django serializers provides functionality to validate our input
        if serializer.is_valid():

            # name in argument is same as defined in serialzer.py
            # We can use other objects too
            name = serializer.validated_data.get('name')

            # We create a message that we retun from API
            # It contain message that we got from request
            message = f'Hello {name}'
            return Response({'message':message})

        # Return 400 Bad Request in case input is not validated
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST    # Or we can pass 400 as int
            )
    
    # PUT Function
    # pk is primary key for specific url
    # Generally put id of object into pk that you are updating
    def put(self, request, pk = None):
        """Handle Updating an object"""

        # Just to demostrate return the response
        return Response({'method':'PUT'})

    def patch(self,request, pk = None):
        """Handle Partial update of an object"""

        # Here we update only the fields provided in request like last name
        return Response({'method':'PATCH'})

    def delete(self, request, pk = None):
        """Handle deleting an object"""
        return Response({'method':'DELETE'})

class FirstViewSet(viewsets.ViewSet):
    """My First API ViewSet"""

    # The methods will basically be typical actions that api will perform
    # Instead of HTTP functions

    # This will list set of objects that  viewset will perform
    def list(self, request):
        """Return list of Objects"""
        a_viewset = [
            'Uses Actions (list, Create,Retrieve, update, update_partially)',
            'Automatically maps URLS using Routers',
            'Provides more functionality with less Code',
        ]
        message = 'Inside list action of viewset'

        return Response({'message':message, 'a_viewset':a_viewset})
    
    # 
    def create(self, request):
        """Create new Message"""

        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'{name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    # Retrieve only specific functions for viewset
    def retrieve(self,request,pk=None):
        """Handle getting object by its ID"""
        return Response({'http-method':'GET'})

    def update(self, request , pk = None):
        """Handle updating whole obejct"""
        return Response({'http-method':'PUT'})

    def update_partially(self, request, pk = None):
        """Handle updating part of object"""
        return Response({'http-method':'PATCH'})

    def delete(self, request, pk = None):
        """Handle Deletng an object with pk"""
        return Response({'http-method':'DELETE'})

class UserViewSet(viewsets.ModelViewSet):
    """Handle creating and managing user profiles"""

    # Like regular connect it to serializer class
    # Then provide query set to model viewset
    # So it knows which objects will be managed through this viewset
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    
    # Set UserProfileViewSet to use correct Auth and Permission classes
    # Can Configure to use one or more Auth types in a viewset auth class tuple
    authentication_classes = (TokenAuthentication,)

    # This sets how user will get permissions for certain things
    permission_classes = (permissions.UpdateOwnProfile,)

    # Add filters to search profiles based on name or email
    filter_backends = (filters.SearchFilter,)

    # Class variable search_fields tells filter_backends
    # Which fields will be searchable by filter
    search_fields = ('name', 'email',)
    
class UserLoginApiView(ObtainAuthToken):
    """Handle creating Auth creation Tokens"""
    # This by default doesn't allow itself to be viewed in browsable djando Admin
    # Hence we will override this class
    # Get default rendered class from API settings
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class SoftwareViewSet(viewsets.ModelViewSet):
    """Create and edit Software Profiles only by Admin"""
    serializer_class = serializers.SoftwareProfileSerializer
    queryset = models.SoftwareProfile.objects.all()
    permission_classes = (permissions.CreateSoftware,)

class ActivationViewSet(viewsets.ModelViewSet):
    """View and Edit Activation List"""
    serializer_class = serializers.ActivationListSerializer
    queryset = models.ActivationList.objects.all()
    permission_classes = (permissions.ViewActivation,)





# class UserProfileFeedApiViewSet(viewsets.ModelViewSet):
#     """CRUD profile feed items"""
#     # We use Token Authentication to authenticate request endpoint
#     authentication_classes = (TokenAuthentication,)
#     serializer_class = serializers.ProfileFeedSerializer
#     # Query set that is managed through this viewset
#     queryset = models.ProfileFeedItem.objects.all()
#     permission_classes = (
#         permissions.UpdateOwnFeed,
#         # Allow anonymous user to see feed : IsAuthenticatedOrReadOnly,
#         IsAuthenticated

#     )

#     def perform_create(self, serializer):
#         """Sets user profile to logged in User"""
#         # Called on whenever POST request is made
#         # Perform create is feature of Django allowing to override behaviour
#         # And customize creating objects through model viewset
#         # Every request is passes to serializer class and validated and .save function is called by default
#         # that save content of serializer to database objects And Here we customize this
#         # The user in user field is added whenever a user is authenticated else set to anonymous user
#         serializer.save(user_profile = self.request.user)

#         return super().perform_create(serializer)