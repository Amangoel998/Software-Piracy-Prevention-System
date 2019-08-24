from rest_framework import serializers


class FirstSerializer(serializers.Serializer):
    """Seriallzes Namefield to test APIView"""
    
    # Accept Name input and add this to APIView
    # Then use to test our POST functionality
    # Define a serialzer and specify inputs fields
    # Define Name that is passed into request which will be validated by serializer

    name = serializers.CharField(max_length = 10)