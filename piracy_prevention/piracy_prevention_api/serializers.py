from rest_framework import serializers
from piracy_prevention_api import models


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
        fields = ('id', 'name', 'email', 'password')

        # Dictionary with keys for custom configuration
        extra_kwargs = {
            'password': {
                'write_only' : True ,
                # To hide it when we enter it
                'style': {'input_type' : 'password' }
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
