from application.database import User, db
from faker import Faker


def test_add_users(app, create_5_users):

    assert User.record_count() == 5