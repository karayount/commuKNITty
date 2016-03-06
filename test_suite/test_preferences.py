
import unittest

class PreferencesTest(unittest.TestCase):
    """ Unit tests for preferences functions """

    def test_group_user_prefs(self):
        """  """

        pass

    def test_update_user_preference(self):
        """ """

        #TODO this one requires a user in the session (see if others do?)
        pass


def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(PreferencesTest("test_group_user_prefs"))
    suite.addTest(PreferencesTest("test_update_user_preference"))

    return suite