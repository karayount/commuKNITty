""" Test suite for CommuKNITty webapp. """

import unittest
import json
from model import connect_to_db, db, create_example_data
from server import app
from jinja_filters import prettify_preference
from seed import load_preferences, load_user_preferences
from local import get_businesses_from_yelp, YelpBusiness, create_map_markers

# assertEqual(a, b)	a == b
# assertNotEqual(a, b)	a != b
# assertTrue(x)	bool(x) is True
# assertFalse(x)	bool(x) is False
# assertIs(a, b)	a is b
# assertIsNot(a, b)	a is not b
# assertIsNone(x)	x is None
# assertIsNotNone(x)	x is not None
# assertIn(a, b)	a in b
# assertNotIn(a, b)	a not in b
# assertIsInstance(a, b)	isinstance(a, b)
# assertNotIsInstance(a, b)  	not isinstance(a, b)


class FlaskTests(unittest.TestCase):
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
        load_preferences("test_data/preference_data.txt")
        load_user_preferences("test_data/user_preference_data.txt")

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

    def test_get_markers(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def tests_find_yarn_matches(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)


class FlaskTestsLoggedIn(unittest.TestCase):
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
        load_preferences("test_data/preference_data.txt")
        load_user_preferences("test_data/user_preference_data.txt")

        with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = 'u1'
                # c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')

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

    def test_show_homepage(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_show_local(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_show_user_profile(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_update_preference_in_db(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_show_basket(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_add_yarn_to_basket(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_show_search_page(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_yarn_driven_search(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_show_parameter_search_results(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)

    def test_show_preference_search_results(self):
        """  """

        test_client = self.client
        # result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        # self.assertIn('<h1>Test</h1>', result.data)



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


class LocalPageTests(unittest.TestCase):
    """ Unit tests about local page"""

    def test_get_businesses_from_yelp(self):
        """ Can we build list of YelpBusiness objects? """

        business_list = get_businesses_from_yelp()
        self.assertIsInstance(business_list[0], YelpBusiness)
        self.assertEqual(business_list[0].biz_name, 'ImagiKnit')

    def test_create_map_markers(self):
        """ Can we create map markers? """

        markers = create_map_markers()
        self.assertIsInstance(markers, dict)


class PatternSearchTests(unittest.TestCase):
    """ Unit tests about search functions """

    def test_build_pattern_list_from_yarn(self):
        """  """

        pass

    def test_build_parameter_search_url(self):
        """  """

        pass

    def test_search_patterns_from_ravelry(self):
        """  """

        #TODO mock API call
        pass

    def test_build_pattern_list_from_parameters(self):
        """  """

        #TODO mock API call, or use one from above function
        pass


class PreferencesTests(unittest.TestCase):
    """ Unit tests for preferences functions """

    def test_group_user_prefs(self):
        """  """

        pass

    def test_get_all_grouped_prefs(self):
        """  """

        get_all_grouped_prefs()

    def test_update_user_preference(self):
        """ """

        #TODO this one requires a user in the session (see if others do?)
        pass


class JinjaFilterTests(unittest.TestCase):
    """ Unit tests about Jinja filters """

    def test_prettify_preference(self):
        """  """

        pass


class SeedTests(unittest.TestCase):
    """ Unit tests for seeding data functions """

    def test_load_users_and_create_baskets(self):
        """  """

        load_users_and_create_baskets("test_data/user_data.txt")

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


if __name__ == '__main__':
    # If called like a script, run our tests

    unittest.main()



#
# """Test suite for Parktake app."""
#
# class ParkTests(unittest.TestCase):
#     """Tests for Parktake app for functions that don't require sessions."""
#
#     def setUp(self):
#         # set up fake test browser
#         self.client = app.test_client()
#
#         # connect to temporary database
#         connect_to_db(app, "sqlite:///")
#
#         # This line makes a 500 error in a route raise an error in a test
#         app.config['TESTING'] = True
#
#         # create tables and add sample data
#         db.create_all()
#         example_data_rec_areas()
#         example_data_users()
#         example_data_visits()
#
#     #############################################################################
#     # Test any functions that only render a template.
#
#     def test_load_homepage(self):
#         """Tests to see if the index page comes up."""
#
#         result = self.client.get('/')
#         # print dir(result) to see what methods are available for result
#
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('text/html', result.headers['Content-Type'])
#         self.assertIn('<a href="https://ridb.recreation.gov">Recreation Information Database</a>', result.data)
#
#     def test_load_signup(self):
#         """Tests to see if the signup page comes up."""
#
#         result = self.client.get('/signup')
#
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('text/html', result.headers['Content-Type'])
#         self.assertIn('Please register for an account.', result.data)
#
#     def test_load_login(self):
#         """Tests to see if the login page comes up."""
#
#         result = self.client.get('/login')
#
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('text/html', result.headers['Content-Type'])
#         self.assertIn('Please log in.', result.data)
#
#     def test_load_about(self):
#         """Tests to see if the about page comes up."""
#
#         result = self.client.get('/about')
#
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('text/html', result.headers['Content-Type'])
#         self.assertIn('Parktake was inspired by a love of adventure.', result.data)
#
#     def test_load_logout(self):
#         """Tests to see if logout occurs properly."""
#
#         result = self.client.get('/logout')
#
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('text/html', result.headers['Content-Type'])
#         self.assertIn('<a id="nav-login" href="/login">Log In</a>', result.data)
#
#     #############################################################################
#     # Test any functions that will query data.
#
#     def test_process_signup_new_user(self):
#         """Test to see if the signup form will process new user properly."""
#
#         result = self.client.post('/process-signup',
#                                   data={'first_name': "Jane",
#                                         'last_name': "Smith",
#                                         'zipcode': "94306",
#                                         'email': "jane@jane.com",
#                                         'password': 'password'},
#                                   follow_redirects=True)
#         self.assertIn('<a href="/view-park" class="view-parks">View Your Parks</a>', result.data)
#         self.assertNotIn('<a id="nav-login" href="/login">Log In</a>', result.data)
#
#     def test_process_signup_known_user(self):
#         """Test to see if the signup form will process a user currently in the database properly."""
#
#         result = self.client.post('/process-signup',
#                                   data={'first_name': "Jane",
#                                         'last_name': "Smith",
#                                         'zipcode': "94306",
#                                         'email': "admin@maynard.com",
#                                         'password': 'password'},
#                                   follow_redirects=True)
#         self.assertIn('/login', result.data)
#         self.assertNotIn('Welcome, ', result.data)
#         self.assertIn('You already have an account. Please login', result.data)
#
#     def test_process_login_known(self):
#         """Test to see if the login form will process properly with a known user."""
#
#         result = self.client.post("/process-login",
#                                   data={"email": 'lucy@test.com', 'password': 'brindlepuppy'},
#                                   follow_redirects=True)
#
#         self.assertIn('Welcome back, Lucy!', result.data)
#         self.assertNotIn('Log In', result.data)
#         self.assertNotIn('Please enter a valid email or password.', result.data)
#
#     def test_process_login_unknown(self):
#         """Test to see if the login form will process properly with an unknown user."""
#
#         result = self.client.post("/process-login",
#                                   data={"email": 'acky@test.com', 'password': 'acky'},
#                                   follow_redirects=True)
#
#         self.assertNotIn('Welcome back,', result.data)
#         self.assertIn('Log In', result.data)
#         self.assertIn('Please enter a valid email or password.', result.data)
#
#     def test_process_login_bad_pwd(self):
#         """Test to see if the login form will process properly with a known user and wrong password."""
#
#         result = self.client.post("/process-login",
#                                   data={"email": 'lucy@test.com', 'password': 'WRONG'},
#                                   follow_redirects=True)
#
#         self.assertNotIn('Welcome back,', result.data)
#         self.assertIn('Log In', result.data)
#         self.assertIn('That email and password combination does not exist.', result.data)
#
#
#
#     def test_show_account_not_logged_in(self):
#         """Test to see if account page will show up if a user isn't logged in."""
#
#         result = self.client.get("/account")
#
#         self.assertNotIn('Your Account', result.data)
#         self.assertIn('/login', result.data)
#
#     def test_save_account_not_logged_in(self):
#         """Test to see if save account page will show up if a user is not logged in."""
#
#         result = self.client.post('/save-changes', data={'first_name': 'Lucy',
#                                                          'last_name': 'Vo',
#                                                          'email': 'lucy@test.com',
#                                                          'password': 'squirrel',
#                                                          'zipcode': '94306'},
#                                                    follow_redirects=True)
#
#         self.assertNotIn('Your account has been updated.', result.data)
#         self.assertNotIn('Lucy', result.data)
#         self.assertIn('/login', result.data)
#
#     #############################################################################
#     # Test any functions to see if they're an instance of a built-in class
#
#     def test_get_parks(self):
#         """Test to see if this function returns a dictionary."""
#
#         visited_parks = db.session.query(Rec_Area).join(Visited_Park).filter(Visited_Park.user_id == 2).all()
#
#         self.assertIsInstance(get_parks(visited_parks), dict)
#
# class ParkTestsSession(unittest.TestCase):
#     """Tests for Parktake app for functions that don't require sessions."""
#
#
#     #############################################################################
#     # Test any functions that only render a template.
#
#     def test_load_landing(self):
#         """Tests to see if the landing page comes up."""
#
#         result = self.client.get('/landing', data={'mapkey': mapkey}, follow_redirects=True)
#
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('text/html', result.headers['Content-Type'])
#         self.assertIn('Your Parks', result.data)
#
#     #############################################################################
#     # Test any functions that will query data.
#
#     def test_process_login_already_logged(self):
#         """Test to see if the login form will show if user is already logged in."""
#
#         result = self.client.get('/login')
#
#         self.assertIn('You are already logged in', result.data)
#
#     def test_show_account_logged_in(self):
#         """Test to see if account page will show up if a user is logged in."""
#
#         result = self.client.get('/account')
#
#         self.assertIn('Your Account', result.data)
#         self.assertIn('Lucy', result.data)
#         self.assertNotIn('/login', result.data)
#
#     def test_update_account_logged_in(self):
#         """Test to see if update account page will show up if a user is logged in."""
#
#         result = self.client.get('/update-account')
#
#         self.assertIn('Update Your Account', result.data)
#         self.assertIn('Lucy', result.data)
#         self.assertNotIn('/login', result.data)
#
#     def test_save_account_logged_in(self):
#         """Test to see if save account page will show up if a user is logged in."""
#
#         result = self.client.post('/save-changes', data={'first_name': 'Lucy',
#                                                    'last_name': 'Vo',
#                                                    'email': 'lucy@test.com',
#                                                    'password': 'squirrel',
#                                                    'zipcode': '94306'},
#                                              follow_redirects=True)
#
#         self.assertIn('Your account has been updated.', result.data)
#         self.assertIn('Lucy', result.data)
#         self.assertNotIn('/login', result.data)
#
#     def test_view_park(self):
#         """Test to see if user can view their visited parks if s/he is logged in."""
#
#         result = self.client.get('/view-park')
#
#         self.assertIn('Based on where you\'ve been,', result.data)
#
#     def test_add_park(self):
#         """Test to see if a park will post to the database properly."""
#
#         result = self.client.post('/add-park', data={'park-id': '2941'},
#                                                follow_redirects=True)
#
#         self.assertIn('Park Added', result.data)
#
#     #############################################################################
#     # Test any functions to see if they're an instance of a built-in class
#
#     def test_parks_json(self):
#         """Test to see if /parks.json route will return json object."""
#
#         response = self.client.get("/parks.json")
#
#         self.assertIsInstance(response, object)
#
#     def test_visited_parks_json(self):
#         """Test to see if /parks-visited.json route will return json object."""
#
#         response = self.client.get("/parks-visited.json")
#
#         self.assertIsInstance(response, object)
#
#     def test_get_chart_data(self):
#         """Test to see if /parks-visited.json route will return json object."""
#
#         response = self.client.get("/parks-in-states.json")
#
#         self.assertIsInstance(response, object)
#
#     #############################################################################
#     # Test suggestion feature
#
#     def test_suggestion_feature(self):
#         """
#         Test to see if the proper park suggestion is offered.
#         Test Users 1 and 2 have almost the same visit history, except for one park each.
#         Test User 2 should get Zion National Park as her suggestion, as that's the only
#         park that deviates from Test User 1's visit history.
#         """
#
#         response = self.client.get("/suggest-park")
#
#         self.assertIn('Zion National Park', response.data)