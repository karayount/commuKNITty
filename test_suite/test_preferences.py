""" Unit tests for functions in preferences module """

import unittest
from server import app
from model import db, connect_to_db, User, UserPreference
from jinja2 import StrictUndefined
from test_model import create_example_data
from seed import load_user_preferences, load_group_events, load_preferences
from preferences import (group_user_prefs, GroupedPreferences,
                         update_user_preference)


class PreferencesTest(unittest.TestCase):
    """ Unit tests for preferences functions """

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
        # create db records for yarns, users, baskets, basket_yarns,
        #                       projects, and patterns
        create_example_data()
        # create db records for preferences and user_preferences
        load_preferences("test_data/preference_data.txt")
        load_user_preferences("test_data/user_preference_data.txt")
        load_group_events("test_data/group-events.csv")

        with self.client as c:
            with c.session_transaction() as session:
                session['username'] = 'u1'

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_group_user_prefs(self):
        """ From a User object can a GroupedPreferences object be returned? """

        user = User.query.filter(User.username == 'u1').first()
        grouped_prefs = group_user_prefs(user)
        self.assertIsInstance(grouped_prefs,GroupedPreferences)

    def test_update_user_preference(self):
        """ Can we add a new UserPreference to database? """

        with self.client as c:
            with c.session_transaction() as session:
                session['username'] = 'u1'
        print session.get("username")
        preference = 'pa-stranded'
        include = 1
        update_user_preference(preference, include)
        new_pref = UserPreference.query.filter(
            UserPreference.user_id == 1,
            UserPreference.pref_id == 26).one()
        self.assertIsNotNone(new_pref)


def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(PreferencesTest("test_group_user_prefs"))
    # suite.addTest(PreferencesTest("test_update_user_preference"))

    return suite