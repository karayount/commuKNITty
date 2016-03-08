import unittest
from jinja_filters import prettify_preference


class JinjaFilterTest(unittest.TestCase):
    """ Unit tests about Jinja filters """

    def test_prettify_preference(self):
        """ Does function convert string? """

        string1 = prettify_preference("test_string_1")
        string2 = prettify_preference("the second test")
        self.assertEqual(string1, "Test")
        self.assertEqual(string2, "The")


def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(JinjaFilterTest("test_prettify_preference"))

    return suite
