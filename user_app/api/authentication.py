from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class BearerAuthentication(authentication.TokenAuthentication):
    keyword = 'Token'

#----------------------Custom Authentication----------------------------

class CustomBasicAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # No header provided, return None for default behavior

        try:
            # Assuming the header format is "Custom <token>"
            auth_type, token = auth_header.split()
            if auth_type != 'Custom':
                return None  # Not the right type

            # Implement your token validation logic
            user = self.get_user_from_token(token)
            if user is None:
                raise AuthenticationFailed('Invalid token')

            return (user, None)  # Return user and None for the second parameter

        except ValueError:
            raise AuthenticationFailed('Invalid authorization header format')

    def get_user_from_token(self, token):
        # Your logic to get the user from the token
        try:
            user = User.objects.get(auth_token=token)  # Adjust according to your model
            return user
        except User.DoesNotExist:
            return None
        
    def authenticate_header(self, request):
        return 'Custom'  # Return the authentication type for the WWW-Authenticate header