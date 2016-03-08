""" This module tests functions in server.py, primarily routes """

import unittest
from server import app, verify_login
from jinja2 import StrictUndefined
from jinja_filters import prettify_preference
from test_model import create_example_data
from model import connect_to_db, db, User, UserPreference, BasketYarn
from seed import load_preferences, load_user_preferences, load_group_events

class FlaskTest(unittest.TestCase):
    """ Tests of Flask routes that don't require logged in user """

    def setUp(self):
        """Setup to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.jinja_env.undefined = StrictUndefined
        app.jinja_env.filters['prettify_preference'] = prettify_preference

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

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_show_landing_page(self):
        """ Does landing page render? """

        test_client = self.client
        result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('CommuKNITty', result.data)

    def test_process_login(self):
        """ Does login add user to session and redirect to home? """

        test_client = self.client
        result = test_client.post('/process_login',
                                  data={'username': 'u1'},
                                  follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn("Welcome,", result.data)
        self.assertIn("/home", result.data)

    def test_get_businesses_for_markers(self):
        """ Does the route return a json object of map markers? """

        test_client = self.client
        result = test_client.get('/get_businesses_for_markers.json')

        self.assertEqual(result.status_code, 200)
        self.assertIn('json', result.headers['Content-Type'])
        self.assertIn('biz_addr', result.data)
        self.assertIn('{', result.data)
        self.assertNotIsInstance(result.data, dict)

    def test_find_yarn_matches(self):
        """ Does route return JSON object of Yarn objects? """

        test_client = self.client
        result = test_client.post('/find_yarn_matches.json',
                                  data = {"yarn_name": "Merino"})

        self.assertEqual(result.status_code, 200)
        self.assertIn('json', result.headers['Content-Type'])
        self.assertIn('yarn', result.data)
        self.assertIn('{', result.data)
        self.assertNotIsInstance(result.data, dict)

    def test_verify_login_fail(self):
        """ Without logged in user, are we prevented from viewing profile? """

        test_client = self.client
        result = test_client.get('/profile')

        self.assertEqual(result.status_code, 302)
        self.assertIn('text/html', result.headers['Content-Type'])


class FlaskTestLoggedIn(unittest.TestCase):
    """ Tests of Flask routes that require a logged in user """

    def setUp(self):
        """Setup to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # secret key to allow sessions to be used
        app.config['SECRET_KEY'] = 'sekrit!'

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        # create db records for yarns, users, baskets, basket_yarns,
        #                       projects, and patterns
        create_example_data()
        # create db records for preferences and user_preferences
        load_preferences("test_data/preference_data.txt")
        load_user_preferences("test_data/user_preference_data.txt")

        with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = 'u1'

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_verify_login(self):
        """ Can we verify whether there is a username attached to session? """

        session = {'username': "u1"}
        user = verify_login(session)
        self.assertIsInstance(user, User)

    def test_process_logout(self):
        """ Can user log out and be redirected to landing page? """

        test_client = self.client
        result = test_client.get('/process_logout',
                                 follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn("now logged out", result.data)

    def test_show_homepage(self):
        """ Can we render the homepage with a logged in user """

        test_client = self.client
        result = test_client.get('/home')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('yarny', result.data)

    def test_show_local(self):
        """ Can we render the Nearby tab? """

        test_client = self.client
        result = test_client.get('/local')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Local knitterly resources', result.data)

    def test_show_user_profile(self):
        """ Can we show a logged in user their profile? """

        test_client = self.client
        result = test_client.get('/profile')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Techniques you enjoy', result.data)

    def test_update_preference_in_db(self):
        """ Does database update and return an id for JS to update page? """

        test_client = self.client
        payload = {'preference': 'pa-stranded', 'include': 1}
        result = test_client.post('/update_preference', data=payload)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('-', result.data)
        self.assertNotIsInstance(result.data, dict)
        new_pref = UserPreference.query.filter(
            UserPreference.user_id == 1,
            UserPreference.pref_id == 26).one()
        self.assertIsNotNone(new_pref)

    def test_show_basket(self):
        """ Does Basket page render for logged in user? """

        test_client = self.client
        result = test_client.get('/basket')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Add more yarn', result.data)

    def test_add_yarn_to_basket(self):
        """ Can new basket yarn be created? """

        test_client = self.client
        payload = {
            "yarn_select": 3,
            "yardage": 1111,
            "colorway": "test_color"
        }
        result = test_client.post('/add_yarn_to_basket', data=payload)

        new_yarn = BasketYarn.query.filter(BasketYarn.yarn_id == 2,
                                           BasketYarn.basket_id == 1).one()

        self.assertEqual(result.status_code, 302)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIsNotNone(new_yarn)


    def test_show_search_page(self):
        """ Does search page render with personalized recommendations? """

        test_client = self.client
        result = test_client.get('/search')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('something specific?', result.data)

    def test_yarn_driven_search(self):
        """ Does db query on yarn return patterns to make with that yarn? """

        test_client = self.client
        basket_yarn_id = 2
        route = '/yarn_driven_search/' + str(basket_yarn_id)
        result = test_client.get(route)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('What to make with', result.data)

    def test_show_parameter_search_results(self):
        """ Do custom pattern results render from input search parameters? """

        test_client = self.client
        payload = {
            "pc": ["cardigan", "beanie-toque"],
            "fit": ["adult", "baby"],
            "weight": ["worsted", "aran"],
            "pa": ["cables", "lace"],
        }
        result = test_client.post('/parameter_search_results', data=payload)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Pattern results from your search', result.data)

    def test_show_preference_search_results(self):
        """ Do personalized pattern results render from user pref params? """

        test_client = self.client
        payload = {
            "pc": ["cardigan", "beanie-toque"],
            "fit": ["adult", "baby"],
            "weight": ["worsted", "aran"],
            "pa": ["cables", "lace"],
        }
        result = test_client.get('/preference_search_results', data=payload)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Personalized recommendations', result.data)


def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()

    suite.addTest(FlaskTest("test_show_landing_page"))
    suite.addTest(FlaskTest("test_get_businesses_for_markers"))
    suite.addTest(FlaskTest("test_process_login"))
    suite.addTest(FlaskTest("test_find_yarn_matches"))
    suite.addTest(FlaskTest("test_verify_login_fail"))
    suite.addTest(FlaskTestLoggedIn("test_process_logout"))
    suite.addTest(FlaskTestLoggedIn("test_verify_login"))
    suite.addTest(FlaskTestLoggedIn("test_show_homepage"))
    suite.addTest(FlaskTestLoggedIn("test_show_local"))
    suite.addTest(FlaskTestLoggedIn("test_show_user_profile"))
    suite.addTest(FlaskTestLoggedIn("test_update_preference_in_db"))
    suite.addTest(FlaskTestLoggedIn("test_show_basket"))
    suite.addTest(FlaskTestLoggedIn("test_add_yarn_to_basket"))
    suite.addTest(FlaskTestLoggedIn("test_show_search_page"))
    suite.addTest(FlaskTestLoggedIn("test_yarn_driven_search"))
    suite.addTest(FlaskTestLoggedIn("test_show_parameter_search_results"))
    suite.addTest(FlaskTestLoggedIn("test_show_preference_search_results"))

    return suite
