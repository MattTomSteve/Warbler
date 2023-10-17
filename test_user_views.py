import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows

os.environ['DATABASE_URL'] = 'postgresql:///warbler-test'

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class MessageViewTestCase(TestCase):

    def setup(self):

        db.drop_all()
        db.create_all()
        