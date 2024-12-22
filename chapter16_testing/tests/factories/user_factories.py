import factory
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")  # Generate random username
    email = factory.Faker("email")  # Generate random email
    first_name = factory.Faker("first_name")  # Generate random first name
    last_name = factory.Faker("last_name")  # Generate random last name
    password = factory.PostGenerationMethodCall("set_password", "password")  # Default password: 'password'
    is_active = True  # Randomly True or False
    is_staff = factory.Faker("pybool")  # Randomly True or False
