
import unittest
from local import get_businesses_from_yelp, build_dict_for_markers, YelpBusiness

class NearbyTest(unittest.TestCase):
    """ Unit tests about local page"""

    def test_get_businesses_from_yelp(self):
        """ Can we build list of YelpBusiness objects? """

        location = "San Francisco"
        business_list = get_businesses_from_yelp(location)
        self.assertIsInstance(business_list[0], YelpBusiness)
        self.assertEqual(business_list[0].biz_name, 'ImagiKnit')

    def test_build_dict_for_markers(self):
        """ Can we create dictionary? """

        location = "San Francisco"
        markers = build_dict_for_markers(location)
        self.assertIsInstance(markers, dict)


def get_suite():
    """ Build suite of all tests this module to send to main tests.py
    :return: suite of all tests this module
    """

    suite = unittest.TestSuite()
    suite.addTest(NearbyTest("test_get_businesses_from_yelp"))
    suite.addTest(NearbyTest("test_build_dict_for_markers"))

    return suite