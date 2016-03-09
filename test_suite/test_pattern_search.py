""" Unit tests for functions in the pattern_search module """

import unittest
from pattern_search import (build_pattern_list_from_yarn,
                            build_parameter_search_url,
                            search_patterns_from_ravelry,
                            build_pattern_list_from_parameters,
                            build_short_pattern_list_from_parameters,
                            SearchResultPattern)
from server import app
from model import db, connect_to_db, Pattern, User
from jinja2 import StrictUndefined
from test_model import create_example_data
from seed import load_user_preferences, load_group_events, load_preferences
from preferences import group_user_prefs


class PatternSearchTest(unittest.TestCase):
    """ Unit tests about search functions """

    def setUp(self):
        """Setup to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.jinja_env.undefined = StrictUndefined

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

    def test_build_pattern_list_from_yarn(self):
        """ With input BasketYarn, is list of SearchResultPatterns returned? """

        pattern_list = build_pattern_list_from_yarn(basket_yarn_id=2)
        self.assertIsInstance(pattern_list, list)
        first_pattern = pattern_list[0]
        self.assertIsInstance(first_pattern, Pattern)


    def test_build_parameter_search_url(self):
        """ Using grouped preferences of user, is Ravelry API url built? """

        user = User.query.filter(User.username == 'u1').first()
        grouped_prefs = group_user_prefs(user)
        search_url = build_parameter_search_url(grouped_prefs)
        self.assertIn("api.ravelry", search_url)

    def test_search_patterns_from_ravelry(self):
        """ Using search url, can we request patterns from ravelry and build list? """

        search_url = "https://api.ravelry.com/patterns/search.json?pc=cowl&weight=worsted"
        pattern_list = search_patterns_from_ravelry(search_url)
        self.assertIsInstance(pattern_list, list)
        first_pattern = pattern_list[0]
        self.assertIsInstance(first_pattern, SearchResultPattern)

    def test_build_pattern_list_from_parameters(self):
        """ from GroupedPreferences, can a pattern list be returned? """

        user = User.query.filter(User.username == 'u1').first()
        grouped_prefs = group_user_prefs(user)
        pattern_list = build_pattern_list_from_parameters(grouped_prefs)
        self.assertIsInstance(pattern_list, list)
        first_pattern = pattern_list[0]
        self.assertIsInstance(first_pattern, SearchResultPattern)

    def test_build_short_pattern_list_from_parameters(self):
        """ from GroupedPreferences, can a list of 5 patterns be returned? """

        user = User.query.filter(User.username == 'u1').first()
        grouped_prefs = group_user_prefs(user)
        pattern_list = build_short_pattern_list_from_parameters(grouped_prefs)
        self.assertIsInstance(pattern_list, list)
        first_pattern = pattern_list[0]
        self.assertIsInstance(first_pattern, SearchResultPattern)


def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(PatternSearchTest("test_build_pattern_list_from_yarn"))
    suite.addTest(PatternSearchTest("test_build_parameter_search_url"))
    suite.addTest(PatternSearchTest("test_search_patterns_from_ravelry"))
    suite.addTest(PatternSearchTest("test_build_pattern_list_from_parameters"))
    suite.addTest(PatternSearchTest("test_build_short_pattern_list_from_parameters"))

    return suite