from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from chapter3_project_setup.models import WatchList, StreamPlatform, Review

User = get_user_model()

# Base Test Class
class BaseViewSetTest(APITestCase):
    """
    Base test class for ViewSets to handle authentication, common setup,
    and client initialization.
    """
    def setUp(self):
        # Create test user and token for authentication
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        
        # Create test data for WatchList, StreamPlatform, and Review
        self.streamplatform = StreamPlatform.objects.create(
            name="Netflix",
            about="Netflix Streaming Platform",
            website="https://netflix.com"
        )
        
        self.watchlist = WatchList.objects.create(
            title="Test WatchList",
            storyline="Test storyline",
            platform=self.streamplatform,
            category="Drama"
        )
        
        self.review = Review.objects.create(
            review_user=self.user,
            rating=4,
            description="Great movie",
            watchlist=self.watchlist,
            active=True,
            review_date="2023-09-13"
        )

    def authenticate_client(self):
        """Helper method to ensure the client is authenticated."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
    def unauthenticate_client(self):
        """Remove authentication credentials from the client."""
        self.client.credentials()  # Removes token from client

# Test WatchListViewSet
class WatchListViewSetTest(BaseViewSetTest):
    def test_watchlist_get_all(self):
        response = self.client.get("/api/chapter16_testing/watchlists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        
    def test_watchlist_get_all_unauthenticated_user(self):
        self.unauthenticate_client()
        response = self.client.get("/api/chapter16_testing/watchlists/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})        

    def test_watchlist_get_single(self):
        response = self.client.get(f"/api/chapter16_testing/watchlists/{self.watchlist.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.watchlist.title)

    def test_watchlist_create(self):
        data = {
            "title": "Movie1",
            "storyline": "Movie1 Story",
            "platform": 1,
            "category": "MOVIE"
        }
        response = self.client.post("/api/chapter16_testing/watchlists/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WatchList.objects.count(), 2)

    def test_watchlist_update(self):
        data = {"title": "Updated WatchList"}
        response = self.client.patch(f"/api/chapter16_testing/watchlists/{self.watchlist.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.watchlist.refresh_from_db()
        self.assertEqual(self.watchlist.title, "Updated WatchList")

    def test_watchlist_delete(self):
        response = self.client.delete(f"/api/chapter16_testing/watchlists/{self.watchlist.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WatchList.objects.filter(id=self.watchlist.id).exists())

# Test StreamPlatformViewSet
class StreamPlatformViewSetTest(BaseViewSetTest):
    def test_streamplatform_get_all(self):
        #reverse arguments are reverse(basename-list)
        response = self.client.get(reverse("stream-platforms-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_streamplatform_get_single(self):
        #reverse arguments are reverse(basename-detail)
        response = self.client.get(reverse("stream-platforms-detail", args=(self.streamplatform.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.streamplatform.name)

    def test_streamplatform_create(self):
        data = {
            "name": "Amazon Prime",
            "about": "Amazon's streaming service",
            "website": "https://primevideo.com"
        }
        response = self.client.post(reverse("stream-platforms-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StreamPlatform.objects.count(), 2)

    def test_streamplatform_update(self):
        data = {"name": "Updated Platform"}
        response = self.client.patch(reverse("stream-platforms-detail", args=(self.streamplatform.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.streamplatform.refresh_from_db()
        self.assertEqual(self.streamplatform.name, "Updated Platform")

    def test_streamplatform_delete(self):
        response = self.client.delete(reverse("stream-platforms-detail", args=(self.streamplatform.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(StreamPlatform.objects.filter(id=self.streamplatform.id).exists())

# Test ReviewViewSet
class ReviewViewSetTest(BaseViewSetTest):
    def test_review_get_all(self):
        response = self.client.get("/api/chapter16_testing/reviews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_review_get_single(self):
        response = self.client.get(f"/api/chapter16_testing/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], self.review.description)

    def test_review_create(self):
        data = {
            "review_user": self.user.id,
            "rating": 5,
            "description": "Amazing movie!",
            "watchlist": self.watchlist.id,
            "active": True,
            "review_date":"2023-09-14"
        }
        response = self.client.post("/api/chapter16_testing/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)

    def test_review_update_with_no_permission(self):
        data = {"rating": 3, "description": "Average movie"}
        response = self.client.patch(f"/api/chapter16_testing/reviews/{self.review.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {'detail': 'Method "PATCH" not allowed.'})

    def test_review_delete(self):
        response = self.client.delete(f"/api/chapter16_testing/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
