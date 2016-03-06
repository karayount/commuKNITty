from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json


class YelpBusiness(object):
    """ Business objects collected from Yelp API

    include name and location information, to show on map
    """

    def __init__(self, biz_name, biz_addr, biz_city, biz_lat, biz_long, biz_url):
        self.biz_name = biz_name
        self.biz_addr = biz_addr
        self.biz_city = biz_city
        self.biz_lat = biz_lat
        self.biz_long = biz_long
        self.biz_url = biz_url


def get_businesses_from_yelp(location_string):
    """ Search Yelp through API for knitting/yarn, save results to objects

    location_string: the user location string
    :return: list of YelpBusiness objects for input city
    """

    # read API keys
    with io.open('yelp_config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)

    yelp_knitting_category_alias = 'knittingsupplies'

    params = {
        'category_filter': yelp_knitting_category_alias
    }

    yelp_results = client.search(location_string, **params)

    list_of_biz = []

    for business in yelp_results.businesses:
        biz_name = business.name
        biz_addr = business.location.display_address
        biz_city = business.location.city
        biz_lat = business.location.coordinate.latitude
        biz_long = business.location.coordinate.longitude
        biz_url = business.url
        biz_closed = business.is_closed

        # exclude businesses that are closed
        if biz_closed == False:
            new_biz = YelpBusiness(biz_name=biz_name,
                                   biz_addr=biz_addr[0],
                                   biz_city=biz_city,
                                   biz_lat=biz_lat,
                                   biz_long=biz_long,
                                   biz_url=biz_url)
            list_of_biz.append(new_biz)

    return list_of_biz


def build_dict_for_markers(location):
    """ Created dictionary of data for google maps to use for markers
    :return: dictionary of business data
    """

    business_list = get_businesses_from_yelp(location)
    count = 1
    dict = {}
    for business in business_list:
        biz_data = {
            "biz_lat": business.biz_lat,
            "biz_long": business.biz_long,
            "biz_name": business.biz_name,
            "biz_addr": business.biz_addr,
            "biz_city": business.biz_city,
            "biz_url": business.biz_url,
            "biz_num": count,
        }
        dict[str(count)] = biz_data
        count += 1

    return dict
