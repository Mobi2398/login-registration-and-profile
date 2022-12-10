from faker import Faker

from application.database import User, db


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"My IS601" in response.data


def test_about_route(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data