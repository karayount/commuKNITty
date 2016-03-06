
import unittest


class JinjaFilterTest(unittest.TestCase):
    """ Unit tests about Jinja filters """

    def test_prettify_preference(self):
        """  """

        pass


def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(JinjaFilterTest("test_prettify_preference"))

    return suite
