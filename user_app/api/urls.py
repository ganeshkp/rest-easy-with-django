from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api import views
from user_app.api import authentication


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('user-login/', views.CustomAuthTokenView.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]