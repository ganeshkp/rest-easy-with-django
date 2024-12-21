import factory
from chapter3_project_setup.models import WatchList, StreamPlatform
from faker import Faker

fake = Faker()

CATEGORY_CHOICES = (
    ("MOVIE", "MOVIE"),
    ("SERIES", "SERIES"),
)

class WatchListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WatchList

    # Generate fake data for each field
    title = factory.Faker("sentence", nb_words=3)  # Random title with 3 words
    storyline = factory.Faker("paragraph", nb_sentences=2)  # Random storyline with 2 sentences
    platform = factory.SubFactory("StreamPlatformFactory")  # Related StreamPlatform instance
    active = factory.Faker("pybool")  # Randomly True or False
    imdb_rating = factory.Faker("pyfloat", left_digits=1, right_digits=1, min_value=0.0, max_value=10.0)  # Random IMDb rating
    created = factory.Faker("date_time_this_decade", tzinfo=None)  # Random date-time within this decade
    episodes = factory.Faker("random_int", min=1, max=100)  # Random number of episodes
    category = factory.LazyFunction(lambda: fake.random.choice([choice[0] for choice in CATEGORY_CHOICES]))  # Random category
