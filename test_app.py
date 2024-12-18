import pytest
from fastapi.testclient import TestClient
from main import app 

def test_search_real_estate_success():
    """Test the /search endpoint with valid data."""
    client = TestClient(app)
    payload = {
        "search_term": "New York",
        "price_max": 1000000,
        "price_min": 500000,
        "lot_size_min": 1000,
        "lot_size_max": 5000,
        "days_on_market": 30,
        "ranges": []
    }

    response = client.post("/search?website=zillow", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "search_results" in data
    assert "forSaleAverageDaysOnMarket" in data
    assert "soldAverageDaysOnMarket" in data
    assert "numberOfForSale" in data
    assert "numberOfSold" in data

def test_search_real_estate_missing_data():
    """Test the /search endpoint with missing required fields."""
    client = TestClient(app)
    payload = {
        "price_max": 1000000,
        "price_min": 500000
    }

    response = client.post("/search?website=zillow", json=payload)
    
    # Should fail due to missing search_term
    assert response.status_code == 422


def test_search_real_estate_invalid_website():
    """Test the /search endpoint with an invalid website parameter."""
    client = TestClient(app)
    payload = {
        "search_term": "California",
        "price_max": 2000000,
        "price_min": 750000,
        "lot_size_min": 500,
        "lot_size_max": 2500,
        "days_on_market": 90,
        "ranges": []
    }

    response = client.post("/search?website=invalidsite", json=payload)

    # Assuming the get_data function has handling for invalid websites
    assert response.status_code == 200  # Adjust depending on implementation
    data = response.json()
    assert data["status"] == "success" or "error" in data


def test_search_real_estate_empty_results():
    """Test the /search endpoint with a search that yields no results."""
    client = TestClient(app)
    payload = {
        "search_term": "Nonexistent Location",
        "price_max": 1,
        "price_min": 0,
        "lot_size_min": 0,
        "lot_size_max": 0,
        "days_on_market": 0,
        "ranges": []
    }

    response = client.post("/search?website=zillow", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["numberOfForSale"] == 0
    assert data["numberOfSold"] == 0


if __name__ == "__main__":
    pytest.main()
