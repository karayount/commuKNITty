import unittest
from pattern_search import (build_pattern_list_from_yarn,
                            build_parameter_search_url,
                            search_patterns_from_ravelry,
                            build_pattern_list_from_parameters,
                            build_short_pattern_list_from_parameters)


class PatternSearchTest(unittest.TestCase):
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

    def test_build_short_pattern_list_from_parameters(self):
        """  """

        #TODO mock API call, or use one from above function
        pass


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