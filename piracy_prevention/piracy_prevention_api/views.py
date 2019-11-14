from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.settings import api_settings

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.contrib.auth import authenticate
from django.core import exceptions

from . import serializers, models, permissions
from .backends import check_Validity
from datetime import *
import hashlib
import uuid

class ValidationAPIView(APIView):
    def post(self, request):
        try:
            self.requestUser = request.POST['user']
            self.requestPassword = request.POST['password']
            self.requestMachine = request.POST['auth_machine']
            self.requestActivationKey = request.POST['Key']
            self.requestTimeStamp = datetime.strptime(str(request.POST['TimeStamp']), '%Y-%m-%d %H:%M:%S.%f')
        except KeyError:
            pass
            return Response('Invalid Request')
        
        if self.requestTimeStamp - datetime.now() > timedelta(minutes=5):
            return Response("TimeStamp Expired")
        elif True in list( map(lambda x:not x, (
            self.requestUser,
            self.requestActivationKey,
            self.requestMachine,
            self.requestPassword,
            self.requestTimeStamp))):
            return Response("Invalid Request Pattern")
        user = None
        try:
            user = authenticate(
                email=self.requestUser,
                password=self.requestPassword,
                )
            if user is None:
                raise Exception("Invalid")
        except:
            return Response('Incorret User Credentials')
        try:
            _ = uuid.UUID(self.requestMachine)
            activation = models.ActivationList.objects.get(authorized_machine=self.requestMachine)
        except:
            return Response("Requested Machine is not registered")
        exp_date = datetime.strptime(str(activation.expiration_date), '%Y-%m-%d')
        if exp_date < datetime.today():
            return Response("Product Not Activated or Expired")
        elif str(activation.user)!=self.requestUser:
            return Response("Activation Not registered to this User")
        elif str(activation.authorized_machine)!=self.requestMachine:
            return Response("Invalid Activation Key")
        try:
            models.ActivationList.objects.filter(activation_hash=self.requestActivationKey).update(is_activated=True)
            user.is_activated = True
            user.save()
        except:
            return Response("Error in models updation")

        response_message = self.requestUser + self.requestMachine + self.requestActivationKey + datetime.now().strftime('%M')
        hashed_message = hashlib.sha256(response_message.encode())
        return Response(hashed_message.hexdigest())

class AuthenticateEndpointUser(APIView):
    def post(self, request):
        try:
            self.requestUser = request.POST['user']
            self.requestPassword = request.POST['password']
            user = authenticate(
                email=self.requestUser,
                password=self.requestPassword,
                )
        except:
            return Response('Incorret User Credentials')
        if user is not None:
            if user.is_activated:
                response_message = 'You were Very Much Authenticated'+datetime.now().strftime('%M')
                hashed_message = hashlib.sha256(response_message.encode())
                return Response(hashed_message.hexdigest())
            else :
                response_message = 'You are Now Very Much Authenticated'+datetime.now().strftime('%M')
                hashed_message = hashlib.sha256(response_message.encode())
                return Response(hashed_message.hexdigest())
        else:
            return Response('Incorret User Credentials')
        


class FirstViewSet(viewsets.ViewSet):
    """My First API ViewSet"""
    def list(self, request):
        """Return list of Objects"""
        a_viewset = [
            'Uses Actions (list, Create,Retrieve, update, update_partially)',
            'Automatically maps URLS using Routers',
            'Provides more functionality with less Code',
        ]
        message = 'Inside list action of viewset'

        return Response({'message':message, 'a_viewset':a_viewset})
    
    
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

    def retrieve(self,request,pk=None):
        """Handle getting object by its ID"""

        return Response({'http-method':'GET', })

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
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)

    search_fields = ('name', 'email',)
    

class SoftwareViewSet(viewsets.ModelViewSet):
    """Create and edit Software Profiles only by Admin"""
    serializer_class = serializers.SoftwareProfileSerializer
    queryset = models.SoftwareProfile.objects.all()
    #permission_classes = [IsAuthenticated]#IsAdminUser]

class ActivationViewSet(viewsets.ModelViewSet):
    """View and Edit Activation List"""
    serializer_class = serializers.ActivationListSerializer
    queryset = models.ActivationList.objects.all()
    #permission_classes = [IsAuthenticated]

