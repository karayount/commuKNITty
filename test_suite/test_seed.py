""" Unit tests of functions in seed.py """

import unittest
from model import db, connect_to_db, User, Basket
from server import app
from jinja2 import StrictUndefined
from seed import (load_group_events, load_preferences, load_user_preferences,
                  load_basket_yarns, load_users_and_create_baskets)


class SeedTest(unittest.TestCase):
    """ Unit tests for seeding data functions """

    def setUp(self):
        """Setup to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.jinja_env.undefined = StrictUndefined

        # secret key to allow sessions to be used
        app.config['SECRET_KEY'] = 'sekrit!'

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb")

        # start with empty db
        db.drop_all()
        # Create tables and add sample data
        db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_load_users_and_create_baskets(self):
        """ Can users and baskets be added to database tables? """

        load_users_and_create_baskets("test_data/user_data.txt")
        u4 = User.query.filter(User.username == 'u4').first()
        self.assertIsInstance(u4, User)
        b1 = Basket.query.get(1)
        self.assertIsInstance(b1, Basket)

    def test_load_yarns(self):
        """ """

        #TODO this one should mock the API call, perhaps
        pass

    def test_load_preferences(self):
        """  """

        load_preferences("test_data/preference_data.txt")

    def test_load_user_preferences(self):
        """  """

        load_user_preferences("test_data/user_preference_data.txt")

    def test_load_basket_yarns(self):
        """  """

        load_basket_yarns("test_data/basket_yarn_data.txt")

    def test_load_group_events(self):
        """  """

        load_group_events("test_data/group-events.csv")



def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(SeedTest("test_load_users_and_create_baskets"))
    # suite.addTest(SeedTest("test_load_yarns"))
    # suite.addTest(SeedTest("test_load_preferences"))
    # suite.addTest(SeedTest("test_load_user_preferences"))
    # suite.addTest(SeedTest("test_load_basket_yarns"))
    # suite.addTest(SeedTest("test_load_group_events"))

    return suite