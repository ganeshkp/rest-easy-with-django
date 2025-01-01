from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from chapter16_testing.tests.factories.streamplatform_factories import StreamPlatformFactory

class WatchlistExternalViewGetTests(APITestCase):
    
    get_url = reverse("watchlist-external")

    @patch('chapter16_testing.api.views.utils.fetch_watchlist_data')  # Mock fetch_watchlist_data
    @patch('chapter16_testing.api.views.utils.fetch_user_recommendations')  # Mock fetch_user_recommendations
    def test_watchlist_external_get_success(self, mock_fetch_user_recommendations, mock_fetch_watchlist_data):
        # Arrange
        mock_fetch_watchlist_data.return_value = [
            {"id": 1, "title": "Mock Movie A"},
            {"id": 2, "title": "Mock Movie B"}
        ]
        mock_fetch_user_recommendations.return_value = [
            {"id": 3, "title": "Mock Movie C"},
            {"id": 4, "title": "Mock Movie D"}
        ]

        # Act
        response = self.client.get(self.get_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "watchlist": [
                {"id": 1, "title": "Mock Movie A"},
                {"id": 2, "title": "Mock Movie B"}
            ],
            "recommendations": [
                {"id": 3, "title": "Mock Movie C"},
                {"id": 4, "title": "Mock Movie D"}
            ]
        })
        mock_fetch_watchlist_data.assert_called_once()
        mock_fetch_user_recommendations.assert_called_once()

    
class WatchlistExternalViewPostTests(APITestCase):
    
    post_url = reverse("watchlist-external")
    
    def setUp(self):
        self.streamplatform = StreamPlatformFactory()
        
    def tearDown(self):
        self.streamplatform.delete()
    
    @patch('chapter16_testing.api.views.utils.validate_external_watchlist_data')  # Mock validation function
    @patch('chapter16_testing.api.views.utils.notify_external_service')  # Mock notification function
    def test_watchlist_external_post_success(self, mock_notify_external_service, mock_validate_external_watchlist_data):
        # Arrange
        mock_validate_external_watchlist_data.return_value = True  # Simulate valid external validation
        mock_notify_external_service.return_value = {"status": "success", "id": 1}  # Simulate successful notification

        data = {
            "title": "Valid Movie",
            "storyline": "Movie4 Storyline",
            "active": True,
            "platform": self.streamplatform.id,
            "imdb_rating": 2.0,
            "episodes": 0,
            "category": "MOVIE"
        }

        # Act
        response = self.client.post(self.post_url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["watchlist_item"]["title"], "Valid Movie")
        self.assertEqual(response.data["notification"]["status"], "success")

        # Ensure mocked functions were called
        mock_validate_external_watchlist_data.assert_called_once()
        mock_notify_external_service.assert_called_once()

    @patch('chapter16_testing.api.views.utils.validate_external_watchlist_data')
    def test_watchlist_external_post_invalid_data(self, mock_validate_external_watchlist_data):
        # Arrange
        mock_validate_external_watchlist_data.return_value = False  # Simulate invalid external validation

        data = {
            "title": "Invalid Movie",
            "description": "This movie will fail validation",
            "imdb_rating": 3.5
        }

        # Act
        response = self.client.post(self.post_url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid watchlist data")

        # Ensure validation function was called
        mock_validate_external_watchlist_data.assert_called_once()

    @patch('chapter16_testing.api.views.utils.validate_external_watchlist_data')
    @patch('chapter16_testing.api.views.utils.notify_external_service')
    def test_watchlist_external_post_serializer_invalid(self, mock_notify_external_service, mock_validate_external_watchlist_data):
        # Arrange
        mock_validate_external_watchlist_data.return_value = True  # Simulate valid external validation

        data = {
            "description": "Missing required title field",  # Missing 'title'
            "imdb_rating": 4.0
        }

        # Act
        response = self.client.post(self.post_url, data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)  # Check that the error contains 'title'

        # Ensure notification function was not called
        mock_notify_external_service.assert_not_called()
