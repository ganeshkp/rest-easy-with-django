import factory
from chapter3_project_setup.models import StreamPlatform


class StreamPlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StreamPlatform

    # Generate fake data for each field
    name = factory.Faker("company")  # Fake company names as streaming platform names
    about = factory.Faker("text", max_nb_chars=150)  # Random text up to 150 characters
    website = factory.Faker("url")  # Random valid URL