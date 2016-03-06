
import unittest
from server import app
from test_model import create_example_data
from model import connect_to_db, db


class FlaskTest(unittest.TestCase):
    """ Tests of Flask routes that don't require logged in user """

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

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
        load_preferences("test_suite/test_data/preference_data.txt")
        load_user_preferences("test_suite/test_data/user_preference_data.txt")

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

    # def test_get_markers(self):
    #     """ Does the route return a json object of map markers? """
    #
    #     test_client = self.client
    #     result = test_client.get('/get_markers.json')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     self.assertIn('see on Yelp', result.data)
    #     self.assertIn('{', result.data)
    #     self.assertNotIsInstance(result.data, dict)

    def test_find_yarn_matches(self):
        """  """

        test_client = self.client
        result = test_client.get('/find_yarn_matches.json')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('yarn_name', result.data)
        self.assertIn('{', result.data)
        self.assertNotIsInstance(result.data, dict)




class FlaskTestLoggedIn(unittest.TestCase):
    """ Tests of Flask routes that require a logged in user """

    def setUp(self):
        """Stuff to do before every test."""

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
        load_preferences("test_suite/test_data/preference_data.txt")
        load_user_preferences("test_suite/test_data/user_preference_data.txt")

        with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = 'u1'

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_process_logout(self):
        """ Can user log out and be redirected to landing page? """

        test_client = self.client
        result = test_client.get('/process_logout',
                                 follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn("now logged out", result.data)

    # def test_show_homepage(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_show_local(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_show_user_profile(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_update_preference_in_db(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_show_basket(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_add_yarn_to_basket(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_show_search_page(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_yarn_driven_search(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_show_parameter_search_results(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #
    # def test_show_preference_search_results(self):
    #     """  """
    #
    #     test_client = self.client
    #     # result = test_client.get('/')
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('text/html', result.headers['Content-Type'])
    #     # self.assertIn('<h1>Test</h1>', result.data)
    #

def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(FlaskTest("test_show_landing_page"))
    suite.addTest(FlaskTest("test_process_login"))
    suite.addTest(FlaskTest("test_find_yarn_matches"))
    suite.addTest(FlaskTestLoggedIn("test_process_logout"))

    return suite


# class MockFlaskTests(unittest.TestCase):
#     """Flask tests that show off mocking."""
#
#     def setUp(self):
#         """Stuff to do before every test."""
#
#         # Get the Flask test client
#         self.client = app.test_client()
#
#         # Show Flask errors that happen during tests
#         app.config['TESTING'] = True
#
#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")
#
#         # Create tables and add sample data
#         db.create_all()
#         example_data()
#
#         # Make mock
#         def _mock_state_to_code(state_name):
#             return "CA"
#
#         self._old_state_to_code = server.state_to_code
#         server.state_to_code = _mock_state_to_code
#
#     def tearDown(self):
#         """Do at end of every test."""
#
#         server.state_to_code = self._old_state_to_code
#         db.session.close()
#         db.drop_all()
#
#     def test_emps_by_state_with_mock(self):
#         """Find employees in a state."""
#
#         r = self.client.get("/emps-by-state.json?state_name=California")
#
#         # Turn json -> Python dictionary
#         info = json.loads(r.data)
#
#         self.assertEqual(len(info['CA']), 4)
#