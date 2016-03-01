""" Test suite for CommuKNITty webapp. """

import unittest
import json
from model import connect_to_db, db
from server import app
import server

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

    # def setUp(self):
    #     """Stuff to do before every test."""
    #
    #     # Get the Flask test client
    #     self.client = app.test_client()
    #
    #     # Show Flask errors that happen during tests
    #     app.config['TESTING'] = True
    #
    #     # Connect to test database
    #     connect_to_db(app, "postgresql:///testdb")
    #
    #     # Create tables and add sample data
    #     db.create_all()
    #     example_data()
    #
    # def tearDown(self):
    #     """Do at end of every test."""
    #
    #     db.session.close()
    #     db.drop_all()

    def test_landing_page(self):
        test_client = server.app.test_client()
        result = test_client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('CommuKNITty', result.data)

    # def test_find_employee(self):
    #     """Can we find an employee in the sample data?"""
    #
    #     leonard = Employee.query.filter(Employee.name == "Leonard").first()
    #     self.assertEqual(leonard.name, "Leonard")
    #
    # def test_emps_by_state(self):
    #     """Find employees in a state."""
    #
    #     r = self.client.get("/emps-by-state.json?state_name=California")
    #
    #     # Turn json -> Python dictionary
    #     info = json.loads(r.data)
    #
    #     self.assertEqual(len(info['CA']), 4)


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



# class EmpTests(unittest.TestCase):
#     """Unit tests about employees."""
#
#     def test_emp_to_dict(self):
#         """Can employee turn to dictionary?"""
#
#         leonard = Employee(name='Leonard', state='CA')
#         expected = {'state': 'CA',
#                     'id': None,
#                     'dept_code': None,
#                     'name': 'Leonard'}
#         self.assertDictEqual(leonard.to_dict(), expected)
#
#     def test_emp_with_dept_to_dict(self):
#         """Can employee with department turn to a dictionary?"""
#
#         legal = Department(dept_code='legal', dept='Legal', phone='555-1212')
#         leonard = Employee(name='Leonard', state='CA', dept=legal)
#         expected = {'dept': {'dept': 'Legal', 'phone': '555-1212'},
#                     'state': 'CA',
#                     'id': None,
#                     'dept_code': None,
#                     'name': 'Leonard'}
#         self.assertDictEqual(leonard.to_dict(), expected)




#
# class MyAppUnitTestCase(unittest.TestCase):
#     """Examples of unit tests: discrete code testing."""
#
#     def testAdder(self):
#         assert server.adder(1, 1) == 99
#
#     def test_should_add_two_nums(self):
#         self.assertEqual(server.adder(4, 5), 9)
#
#     def test_things(self):
#         self.assertEqual(len(server.things_from_db()), 3)
#
#
# class MyAppIntegrationTestCase(unittest.TestCase):
#     """Examples of integration tests: testing Flask server."""
#
#     def setUp(self):
#         print "(setUp ran)"
#         self.client = server.app.test_client()
#         server.app.config['TESTING'] = True
#
#     def tearDown(self):
#         # We don't need to do anything here; we could just
#         # not define this method at all, but we have a stub
#         # here as an example.
#         print "(tearDown ran)"
#
#     def test_home(self):
#         result = self.client.get('/')
#         self.assertIn('<h1>Test</h1>', result.data)
#
#     def test_adder(self):
#         result = self.client.get('/add-things?x=-1&y=1')
#         self.assertEqual(result.data, "99")
#
#     def test_results(self):
#         result = self.client.get('/')
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('text/html', result.headers['Content-Type'])
#         self.assertIn('<h1>Test</h1>', result.data)

if __name__ == '__main__':
    # If called like a script, run our tests

    unittest.main()
