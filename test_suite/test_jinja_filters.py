
import unittest


class JinjaFilterTest(unittest.TestCase):
    """ Unit tests about Jinja filters """

    def setUp(self):

        print "got to set up"

    def tearDown(self):

        print "tore down"

    def test_prettify_preference(self):
        """  """

        print "test pretty maker"

    def test_another(self):

        print "another test case"


def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(JinjaFilterTest("test_prettify_preference"))
    suite.addTest(JinjaFilterTest("test_another"))

    return suite
