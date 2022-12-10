from faker import Faker

from application.database import User, db


def test_address_field(client, create_5_users):

    response = client.get("/users/1")
    assert response.status_code == 200
    assert b"brian12@example.net" in response.data