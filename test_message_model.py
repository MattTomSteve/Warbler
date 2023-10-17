"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


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

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.uid = 1
        u = User.signup('user1', 'user1@email.com', 'password', None)
        u.id = self.uid
        db.session.commit()

        self.uid2 = 2
        u2 = User.signup('user2', 'user2@email.com', 'password', None)
        u2.id = self.uid2
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):

        m = Message(text = 'test message', 
                    user_id=self.uid)
        
        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, 'test message')

    def test_message_like(self):

        m = Message(text = 'test message',
                     user_id=self.uid)
        
        db.session.add(m)
        db.session.commit()

        # Check likes
        self.assertEqual(len(self.u.likes), 0)

        # Add Like
        self.u.likes.append(m)
        db.session.commit()

        self.assertEqual(len(self.u.likes), 1)
        self.assertEqual(self.u.likes[0].text, 'test message')

        # Remove Like
        self.u.likes.remove(m)
        db.session.commit()
     
        self.assertEqual(len(self.u.likes), 0)


    