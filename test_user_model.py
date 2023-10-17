"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy import exc
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_is_following(self):
        u1 = User.signup('user1', 'user1@email.com', 'password', None)
        u2 = User.signup('user2', 'user2@email.com', 'password', None)
        db.session.add(u1)
        db.session.add(u2)
        u1.following.append(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))

    def test_is_followed_by(self):
        u1 = User.signup('user1', 'user1@email.com', 'password', None)
        u2 = User.signup('user2', 'user2@email.com', 'password', None)
        db.session.add(u1)
        db.session.add(u2)
        u1.followers.append(u2)
        db.session.commit()
        self.assertTrue(u1.is_followed_by(u2))
        self.assertFalse(u2.is_followed_by(u1))

    def test_valid_signup(self):
        u1 = User.signup('user1', 'user1@email.com', 'password', None)
        db.session.commit()
        self.assertIsNotNone(u1.id)
        self.assertEqual(u1.username, 'user1')
        self.assertEqual(u1.email, 'user1@email.com')
        self.assertTrue(u1.password, 'password')

    def test_invalid_signup(self):
        u1 = User.signup(None, 'user1@email.com', 'password', None)
        self.assertIsNone(u1.id)
        with self.assertRaises(exc.IntegrityError) as context:
           db.session.commit()
           User.signup(None, 'user1@email.com', 'password', None)

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None, None)

    def test_valid_auth(self):
        u1 = User.signup('user1', 'user1@email.com', 'password', None)
        db.session.commit()
        expect_uid = 1
        self.assertEqual(u1.id, expect_uid)

    def test_invalid_user(self):
        u1 = User.signup('user1', 'user1@email.com', 'password', None)
        db.session.commit()
        self.assertFalse(User.authenticate('user2', 'password'))

    def test_invalid_password(self):
        u1 = User.signup('user1', 'user1@email.com', 'password', None)
        db.session.commit()
        self.assertFalse(User.authenticate('user1', 'notpassword'))