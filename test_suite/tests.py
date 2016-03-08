""" Test suite for CommuKNITty webapp. """

import unittest
import sys
import test_server
import test_local
import test_pattern_search
import test_preferences
import test_jinja_filters
import test_seed
import test_with_selenium



if __name__ == '__main__':
    # If called like a script, run our tests

    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)

    server_suite = test_server.get_suite()
    local_suite = test_local.get_suite()
    # pattern_search_suite = test_pattern_search.get_suite()
    # preferences_suite = test_preferences.get_suite()
    jinja_filters_suite = test_jinja_filters.get_suite()
    # seed_suite = test_seed.get_suite()
    # selenium_suite = test_with_selenium.get_suite()
    all_tests = unittest.TestSuite([
        server_suite,
        local_suite,
        # pattern_search_suite,
        # preferences_suite,
        jinja_filters_suite,
        # seed_suite,
        # selenium_suite,
    ])

    runner.run(all_tests)
