from rest_framework.views import APIView
from rest_framework.response import Response

# Any Request Made to View is assigned to this
class FirstAPI(APIView):
    """My First API View"""

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