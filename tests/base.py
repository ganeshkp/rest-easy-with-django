from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from tests.factories.user_factories import UserFactory

class BaseAPITests:
    class APITests(APITestCase):
        url = None
        url_string = None
        request_method = None
        factory_class = None
        factory_kwargs = {}
        data = {}
        auth_response_code = status.HTTP_200_OK
        request_kwargs = {}
        
        def setUp(self):
            return super().setUp()
        
        def test_unauthenticated_user(self):
            response = getattr(self.client, self.request_method)(self.url, self.data, **self.request_kwargs)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})
            
        def test_method_authenticated_user(self):
            user = UserFactory()
            self.client.login(username=user.username, password=user.password)
            self.token = Token.objects.get(user__username=user)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
            
            response = getattr(self.client, self.request_method)(self.url, self.data, follow=True, **self.request_kwargs)
            self.assertEqual(response.status_code, self.auth_response_code)
            self.client.logout()     
    
    class APIListTests(APITests):
        request_method="get" 
        
    class APIDetailTests(APIListTests):        
        def setUp(self):
            self.obj = self.factory_class(**self.factory_kwargs)
            self.url = reverse(self.url_string, args=[self.obj.id])
            
        def tearDown(self):
            self.obj.delete
            
    class APIPostTests(APITests):
        request_method="post"
        auth_response_code = status.HTTP_201_CREATED
        
    class APIPutTests(APIDetailTests):
        request_method = "put"
        
    class APIPatchTests(APIDetailTests):
        request_method = "patch"
        
    class APIDeleteTests(APIDetailTests):
        request_method = "delete"
        auth_response_code = status.HTTP_204_NO_CONTENT
