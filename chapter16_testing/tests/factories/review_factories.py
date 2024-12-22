import factory
from chapter3_project_setup.models import Review
from django.contrib.auth import get_user_model
from faker import Faker
from tests.factories.user_factories import UserFactory
from chapter16_testing.tests.factories.watchlist_factories import WatchListFactory

fake = Faker()
User = get_user_model()

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    review_user = factory.SubFactory(UserFactory)  # Related User instance
    rating = factory.Faker("random_int", min=1, max=5)  # Random rating between 1 and 5
    description = factory.Faker("sentence", nb_words=10)  # Random description with 10 words
    watchlist = factory.SubFactory(WatchListFactory)  # Related WatchList instance
    active = factory.Faker("pybool")  # Randomly True or False
    created = factory.Faker("date_time_this_year")  # Random datetime within this year
    update = factory.Faker("date_time_this_year")  # Random datetime within this year
    review_date = factory.LazyFunction(lambda: fake.date_between(start_date='-1y', end_date='today'))  # Random review date within the last year
