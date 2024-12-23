from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from chapter3_project_setup.models import WatchList, StreamPlatform, Review
from chapter16_testing.api.views import WatchListViewSet  # Import your ViewSet here
import unittest

User = get_user_model()


class WatchListViewSetAPITest(unittest.TestCase):
    """Tests for WatchListViewSet using APIRequestFactory."""

    def setUp(self):
        # Create user and token
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create test data for WatchList and StreamPlatform
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
        
    def tearDown(self):
        self.streamplatform.delete()
        self.watchlist.delete()
        self.user.delete()

    def test_list_watchlist_authenticated(self):
        """Test the list endpoint with authenticated user."""
        # Create request
        request = self.factory.get("/api/chapter16_testing/watchlists/")
        force_authenticate(request, user=self.user)

        # Initialize the view and get the response
        view = WatchListViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), WatchList.objects.count())

    def test_list_watchlist_unauthenticated(self):
        """Test the list endpoint without authentication."""
        request = self.factory.get("/api/chapter16_testing/watchlists/")
        view = WatchListViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})        

    def test_create_watchlist_authenticated(self):
        """Test creating a new WatchList with authenticated user."""
        data = {
            "title": "New WatchList",
            "storyline": "New storyline",
            "platform": "1",
            "category": "MOVIE",
        }

        request = self.factory.post("/api/chapter16_testing/watchlists/", data, format="json")
        force_authenticate(request, user=self.user)

        view = WatchListViewSet.as_view({"post": "create"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_create_watchlist_unauthenticated(self):
        """Test creating a new WatchList without authentication."""
        data = {
            "title": "New WatchList",
            "storyline": "New storyline",
            "platform": "1",
            "category": "MOVIE",
        }

        request = self.factory.post("/api/chapter16_testing/watchlists/", data, format="json")
        view = WatchListViewSet.as_view({"post": "create"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_update_watchlist_authenticated(self):
        """Test updating an existing WatchList with authenticated user."""
        data = {"title": "Updated WatchList"}

        request = self.factory.patch(f"/api/chapter16_testing/watchlists/{self.watchlist.id}/", data, format="json")
        force_authenticate(request, user=self.user)

        view = WatchListViewSet.as_view({"patch": "partial_update"})
        response = view(request, pk=self.watchlist.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.watchlist.refresh_from_db()
        self.assertEqual(self.watchlist.title, data["title"])

    def test_delete_watchlist_authenticated(self):
        """Test deleting an existing WatchList with authenticated user."""
        request = self.factory.delete(f"/api/chapter16_testing/watchlists/{self.watchlist.id}/")
        force_authenticate(request, user=self.user)

        view = WatchListViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.watchlist.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WatchList.objects.filter(id=self.watchlist.id).exists())

    def test_delete_watchlist_unauthenticated(self):
        """Test deleting an existing WatchList without authentication."""
        request = self.factory.delete(f"/api/chapter16_testing/watchlists/{self.watchlist.id}/")
        view = WatchListViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.watchlist.id)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

# Test StreamPlatformViewSet
class StreamPlatformViewSetTest(APITestCase):
    def setUp(self):
        # Create test user and token for authentication
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)        
        
        # Create test data for StreamPlatform
        self.streamplatform = StreamPlatform.objects.create(
            name="Netflix",
            about="Netflix Streaming Platform",
            website="https://netflix.com"
        )
        
    def tearDown(self):
        self.streamplatform.delete()
        self.user.delete()
        self.client.logout()

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
class ReviewViewSetTest(APITestCase):
    def setUp(self):
        # Create test user and token for authentication
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.client.login(username=self.user.username, password=self.user.password)
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
        
    def tearDown(self):
        self.streamplatform.delete()
        self.watchlist.delete()
        self.review.delete()
        self.client.logout()

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

    def test_review_update_with_method_not_allowed(self):
        data = {"rating": 3, "description": "Average movie"}
        response = self.client.patch(f"/api/chapter16_testing/reviews/{self.review.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {'detail': 'Method "PATCH" not allowed.'})

    def test_review_delete(self):
        response = self.client.delete(f"/api/chapter16_testing/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())