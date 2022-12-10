"""Testing Registration Routes"""
from flask import url_for

from application import db
from application.database import User


def test_user_registration_success(client):
    with client:
        response = client.post("/registration", data={
            "email": "steve@steve.com",
            "password": "testtest",
            "confirm": "testtest",
        }, follow_redirects=True)

        assert response.request.path == url_for('authentication.login')
        assert response.status_code == 200


def test_user_registration_duplicate_user_fail(app, client):
    with app.app_context():
        user = User.create('steve@steve.com', 'testtest')
        db.session.add(user)
        db.session.commit()

    with client:
        response = client.post("/registration", data={
            "email": "steve@steve.com",
            "password": "testtest",
            "confirm": "testtest",
        }, follow_redirects=True)

        assert response.request.path == url_for('authentication.registration')
        assert response.status_code == 200
        assert b"Already Registered" in response.data

