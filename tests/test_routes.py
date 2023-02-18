import json
import os
import requests


def test_hotel_add_hotel(host_endpoint):
    endpoint = os.path.join(host_endpoint, "hotels").replace("\\", "/")
    response = requests.post(
        endpoint,
        json={
            "name": "Hotel Test",
            "city": "Bogota",
            "address": "Calle Falsa",
            "contact_email": "test@test.com",
            "image_url": "https://i.blogs.es/6c558d/luna-400mpx/450_1000.jpg",
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "id" in json_data
    assert json_data["city"] == "Bogota"


def test_hotel_add_hotel_invalid(host_endpoint):
    endpoint = os.path.join(host_endpoint, "hotels").replace("\\", "/")
    response = requests.post(
        endpoint,
        json={
            "name": "Hotel Test1",
            "city": "Bogota",
            "address": "Calle Falsa",
            "contact_email": "test@test.com",
            "image_url": "https://i.blogs.es/6c558d/luna-400mpx/450_1000.jpg",
        },
    )
    assert response.status_code == 400
    json_data = response.json()
    assert "error" in json_data


def test_hotel_get_hotels_valid(host_endpoint):
    endpoint = os.path.join(host_endpoint, "hotels").replace("\\", "/")
    response = requests.get(endpoint)
    assert response.status_code == 200


def test_hotel_get_hotel_invalid(host_endpoint):
    endpoint = os.path.join(host_endpoint, "hotels", "1").replace("\\", "/")
    response = requests.get(endpoint)
    assert response.status_code == 400
    json_data = response.json()
    assert "error" in json_data


def test_hotel_delete_hotel_invalid(host_endpoint):
    endpoint = os.path.join(host_endpoint, "hotels", "1").replace("\\", "/")
    response = requests.delete(endpoint)
    assert response.status_code == 400
    json_data = response.json()
    assert "error" in json_data
