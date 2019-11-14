from rest_framework import serializers
from . import models


class FirstSerializer(serializers.Serializer):
    """Seriallzes Namefield to test APIView"""
    
    # Accept Name input and add this to APIView
    # Then use to test our POST functionality
    # Define a serialzer and specify inputs fields
    # Define Name that is passed into request which will be validated by serializer

    name = serializers.CharField(max_length = 10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serialize a user profile"""

    # Meta Class configure serializer to point to specific model in project
    class Meta:
        model = models.UserProfile

        # List of fields in model to be managed by serializer
        # These fields we want to make accessible in API
        # Or to create new models with the serializer
        fields = ('id', 'name', 'email', 'password', 'is_activated')

        # Dictionary with keys for custom configuration
        extra_kwargs = {
            'password': {
                'write_only' : True ,
                # To hide it when we enter it
                'style': {'input_type' : 'password' }
            },
            'is_activated':{
                'read_only': False,
            }
        }

    # Now we overwrite the default create function for object manager
    # This customizes how password is saved in hash instead of cleartext

    def create(self, validated_data):
        """Create and return a new user"""
        
        # models.py has UserProfileManager with create_user
        # But aren't using it here
        # user.set_password in UserProfileManager will make password into hash
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user


class ActivationListSerializer(serializers.ModelSerializer):
    """Serializes Software Profile"""

    class Meta:
        model = models.ActivationList
        fields = (
            'software', 'user', 'authorized_machine', 'activation_date', 'expiration_date', 'activation_hash','is_activated'
        )
        extra_kwargs = {
            "software": {
                "required": True,
                "read_only": False,
            },
            "user": {
                "required": True,
                "read_only": False,
            },
            "authorized_machine": {
                "required": True,
                "read_only": False,
            },
            "activation_date": {
                "required": False,
                "read_only": True,
            },
            "expiration_date": {
                "required": True,
                "read_only": False,
            },
            "activation_hash": {
                "required": False,
                "read_only": True,
            },
            "is_activated": {
                "required": False,
                "read_only": True,
            }

        }
        order_by = 'software'

    def create(self, validated_data):
        """Create and return a new software Activation"""
        
        activation = models.ActivationList.objects.create(
            user = validated_data['user'],
            software = validated_data['software'],
            authorized_machine = validated_data['authorized_machine'],
            expiration_date = validated_data['expiration_date'],
        )
        return activation

class SoftwareProfileSerializer(serializers.ModelSerializer):
    """Serialize Software Profiles"""
    class Meta:
        model = models.SoftwareProfile
        fields = (
            'software_name', 'software_organization', 'active_users',
            # or simply '_all_'
        )
        order_by = 'software_organization'
    
    def create(self, validated_data):
        software = models.SoftwareProfile.objects.create(
            software_name = validated_data['software_name'],
            software_organization = validated_data['software_organization'],
        )
        return software
    

