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



def get_businesses_from_yelp():
    """ Search Yelp through API for knitting/yarn, save results to objects
    :return: list of YelpBusiness objects for input city
    """

    # read API keys
    with io.open('yelp_config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)

    params = {
        'category_filter': 'knittingsupplies'
    }

    yelp_results = client.search('San Francisco', **params)

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


def create_map_markers():
    """ Creates dictionary of map marker data to be sent to mapbox
    :return: dictionary of business data for creating mapbox markers
    """

    business_list = get_businesses_from_yelp()
    features = []
    for business in business_list:
        properties = {
            "description": ("<div class=\"marker-title\">" +
                            business.biz_name + "</div><p>" +
                            business.biz_addr + "<br><a href=\"" +
                            business.biz_url + ">see on Yelp</a></p>"),
            "marker-symbol": "marker"
        }
        geometry = {
            "type": "Point",
            "coordinates": [business.biz_long, business.biz_lat]
        }
        feature = {
            "type": "Feature",
            "properties": properties,
            "geometry": geometry
        }
        features.append(feature)

    data = {
        "type": "FeatureCollection",
        "features": features
    }

    markers = {
        "type": "geojson",
        "data": data
    }

    return markers
