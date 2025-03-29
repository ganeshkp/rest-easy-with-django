
def fetch_watchlist_data():
    """
    Simulates fetching data from an external service for the watchlist.
    """
    return [{"id": 1, "title": "Movie A"}, {"id": 2, "title": "Movie B"}]

def fetch_user_recommendations(user_id):
    """
    Simulates fetching user-specific recommendations from another external service.
    """
    return [{"id": 3, "title": "Movie C"}, {"id": 4, "title": "Movie D"}]


def validate_external_watchlist_data(data):
    """
    Simulates validating watchlist data using an external service.
    """
    if data.get("title") == "Invalid Movie":
        return False  # Simulate invalid data from an external service
    return True

def notify_external_service(watchlist_item):
    """
    Simulates notifying an external service after successfully creating a watchlist item.
    """
    # Simulate sending data to an external service
    return {"status": "success", "id": watchlist_item.id}
