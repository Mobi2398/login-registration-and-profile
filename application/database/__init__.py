"""
Database Initialization and Models
"""
from flask import flash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, backref
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class GenericSQLAlchemyMethods:

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def record_count(cls):
        return cls.query.count()

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()


class User(UserMixin, db.Model, GenericSQLAlchemyMethods):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    profile = relationship("Profile", uselist=False, backref="user", cascade="all, delete-orphan")
    groups = relationship("Group", secondary="membership")

    def __init__(self, email, password, active=True):
        self.email = email
        self.password = User.set_password(password)
        self.active = active

    @classmethod
    def create(cls, email, password):
        return cls(email, password)

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.id


class Profile(db.Model, GenericSQLAlchemyMethods):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    phone = db.Column(db.String(12))

    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone


class Group(db.Model, GenericSQLAlchemyMethods):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    users = relationship("User", secondary="membership")

    def __init__(self, title):
        self.title = title


class Membership(db.Model, GenericSQLAlchemyMethods):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    user = relationship(User, backref=backref("membership", cascade="all, delete-orphan"))
    group = relationship(Group, backref=backref("membership", cascade="all, delete-orphan"))
