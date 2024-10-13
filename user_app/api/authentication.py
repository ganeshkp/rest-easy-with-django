from six import text_type
import base64
import binascii

from django.contrib.auth import authenticate, get_user_model
from rest_framework import authentication

from rest_framework import exceptions, HTTP_HEADER_ENCODING


class BearerAuthentication(authentication.TokenAuthentication):
    keyword = 'Token'

#----------------------Custom Authentication----------------------------

def get_authorization_header(request):
    """
        Return request's "Authorization:" header, as a byte string.
        Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get("HTTP_AUTHORIZATION", b"")
    if isinstance(auth, text_type):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth

def decode_header(auth_token, decode_type=HTTP_HEADER_ENCODING):
    """Decodes the header for basic authentication

    Args:
        auth_token : string token to be decoded
        decode_type : string of decoding to be used. Ex. "iso-8859-1". Defaults to HTTP_HEADER_ENCODING.

    Returns:
        List of auth elements [email, ":", password]
    """
    auth_parts = base64.b64decode(auth_token).decode(decode_type).partition(":")
    return auth_parts

class CustomBasicAuthentication(authentication.BasicAuthentication):
    def authenticate_credentials(self, request, userid, password):
        """
            Authenticate the userid and password against username and password
        """
        credentials = {
            get_user_model().USERNAME_FIELD: userid,
            "password": password
        }
        
        # Attempt to authenticate using standard encode, fallback to check with forced UTF-8
        user = authenticate(request, **credentials)        
        return (user, None)
    
    def authenticate(self, request):
        """
            Returns a User if a correct username and password have been supplied using
            HTTP Basic authentication, Otherwise returns None
        """
        auth = get_authorization_header(request).split()
        default_success = True
        utf_success = True
        userid = None
        password = None
        
        if not auth or auth[0].lower() != b"basic":
            return None
        
        if len(auth) == 1:
            msg = ("Invalid basic header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ("Invalid basic header. Credentials string should not contain spaces")
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            auth_parts_utf = decode_header(auth[1], decode_type="utf-8")
        except (TypeError, UnicodeDecodeError, binascii.Error):
            utf_success = False
            
        try:
            auth_parts = decode_header(auth[1])
            userid = auth_parts[0]
            password = auth_parts[2]
        except (TypeError, UnicodeDecodeError, binascii.Error):
            default_success = False
            
        if not default_success and not utf_success:
            msg = ("Invalid basic header. Credentials not correctly encoded.")
            raise exceptions.AuthenticationFailed(msg)
        
        user_object = self.authenticate_credentials(request, userid, password)
        
        if not user_object[0]:
            if utf_success:
                # Try and authenticate with UTF-8
                userid = auth_parts_utf[0]
                password = auth_parts_utf[2]
                user_object = self.authenticate_credentials(request, userid, password)
                if not user_object[0]:
                    raise exceptions.AuthenticationFailed("Invalid username/password")
                return user_object
            raise exceptions.AuthenticationFailed("Invalid username/password")
        
        if not user_object[0].is_active:
            raise exceptions.AuthenticationFailed("Invalid username/password")
        
        return user_object
    
class QuietBasicAuthentication(CustomBasicAuthentication):
    """
        Stops challenging user credentials when invalid details are received
    """
    
    def authenticate_header(self, request):
        return 'xBasic realm="%s"' % self.www_authenticate_realm
