
import unittest

#TODO can these even be tested if they attempt to clear current db?
class SeedTest(unittest.TestCase):
    """ Unit tests for seeding data functions """

    def test_load_users_and_create_baskets(self):
        """  """

        load_users_and_create_baskets("test_suite/test_data/user_data.txt")

    def test_load_yarns(self):
        """ """

        #TODO this one should mock the API call, perhaps
        pass

    def test_load_preferences(self):
        """  """

        load_preferences("test_suite/test_data/preference_data.txt")

    def test_load_user_preferences(self):
        """  """

        load_user_preferences("test_suite/test_data/user_preference_data.txt")

    def test_load_basket_yarns(self):
        """  """

        load_basket_yarns("test_suite/test_data/basket_yarn_data.txt")

    def test_load_group_events(self):
        """  """

        load_group_events("test_suite/test_data/group-events.csv")



def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(SeedTest("test_load_users_and_create_baskets"))
    suite.addTest(SeedTest("test_load_yarns"))
    suite.addTest(SeedTest("test_load_preferences"))
    suite.addTest(SeedTest("test_load_user_preferences"))
    suite.addTest(SeedTest("test_load_basket_yarns"))
    suite.addTest(SeedTest("test_load_group_events"))

    return suite