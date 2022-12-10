"""Testing User Profile """
from flask_login import current_user

from application.database import User, db, Profile, Group


def test_group_model(app, create_5_users):
    with app.app_context():
        assert Group.record_count() == 0
        group = Group("Group One")
        group.save()
        assert Group.record_count() == 1


def test_group_model_join_membership(app, create_5_users):
    with app.app_context():
        assert Group.record_count() == 0
        group = Group("Group One")
        group.save()
        group2 = Group("Group Two")
        group2.save()
        assert Group.record_count() == 2
        user = User.find_by_id(1)
        user.groups = [group, group2]
        user.save()


def test_new_group_post_controller(app, client, login):
    with client:
        response = client.post("/groups/new", data={
            "title": "My Group",
        }, follow_redirects=True)
        assert response.status_code == 200
    with app.app_context():
        assert Group.record_count() == 1
