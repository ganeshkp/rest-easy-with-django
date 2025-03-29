from django.urls import reverse
from tests.base import BaseAPITests
from chapter16_testing.tests.factories.watchlist_factories import WatchListFactory
from chapter16_testing.tests.factories.streamplatform_factories import StreamPlatformFactory

class WatchlistListTests(BaseAPITests.APIListTests):
    url = reverse("watchlists-list")
    
class WatchlistDetailTests(BaseAPITests.APIDetailTests):
    url_string = "watchlists-detail"
    factory_class = WatchListFactory
    
class WatchlistPostTests(BaseAPITests.APIPostTests):
    url = reverse("watchlists-list")
    
    def setUp(self):
        streamplatform = StreamPlatformFactory()
        self.data = {
            "title": "Movie1",
            "storyline": "Movie1 Story",
            "platform": streamplatform.id,
            "category": "MOVIE",
            "imdb_rating":4.0,
            "active": True,
        }
        
class WatchlistPutTests(BaseAPITests.APIPutTests):
    url_string = "watchlists-detail"
    factory_class = WatchListFactory
    
    def setUp(self):
        super(WatchlistPutTests, self).setUp()
        streamplatform = StreamPlatformFactory()
        self.data = {
            "title":"Updated test title", 
            "storyline":"Updated test storyline",
            "platform":streamplatform.id,
            "category":"MOVIE"
        }
        
class WatchlistPatchTests(BaseAPITests.APIPatchTests):
    url_string = "watchlists-detail"
    factory_class = WatchListFactory
    data = {"title":"Updated test title"}
    
class WatchlistDeleteTests(BaseAPITests.APIDeleteTests):
    url_string = "watchlists-detail"
    factory_class = WatchListFactory   
    