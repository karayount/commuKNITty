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


def create_map_markers():
    """ Creates dictionary of map marker data to be sent to mapbox
    :return: dictionary of business data for creating mapbox markers
    """

    location = 'San Francisco'
    business_list = get_businesses_from_yelp(location)
    features = []
    iter = 1
    for business in business_list:
        properties = {
            "title": business.biz_name,
            "description": ("<div class=\"marker-title\">" +
                            business.biz_name + "</div><p>" +
                            business.biz_addr + "<br><a href=\"" +
                            business.biz_url + ">see on Yelp</a></p>"),
            'marker-size': 'large',
            #'marker-color': "#cccccc",
            'marker-color': '#f0a',
            'marker-symbol': str(iter)
            # 'marker-symbol': '1'
            # "marker-symbol": "harbor"
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
        iter += 1

    data = {
        "type": "FeatureCollection",
        "features": features
    }

    markers = {
        "type": "geojson",
        "data": data
    }

    return markers



# #terri's for one marker
# e_geojson = {
#                 "type": "FeatureCollection",
#                 "features": [
#                     {
#                     "type": "Feature",
#                     "properties": {
#                         "title": marker.title,
#                         "date": marker.date,
#                         "date-tier": marker.date_tier,
#                         "time": marker.time,
#                         "name": marker.name,
#                         "address": marker.address,
#                         "cost": marker.cost,
#                         "img_url": marker.img_url,
#                         "event_url": marker.event_url,
#                         "description": marker.description,
#                         "category": marker.category,
#                         "marker-type": marker.marker_type,
#                         "marker-symbol": marker.marker_symbol,
#                         "marker-color": marker.marker_color
#                         },
#                     "geometry": {
#                         "coordinates": [
#                             marker.longitude,
#                             marker.latitude],
#                         "type": "Point"
#                     },
#                     "id": marker.marker_id
#                     }
#                 for marker in Marker.query.filter(Marker.marker_type == 'event', Marker.datetime >= today).all()
#                 ]
#             }
#
#     return jsonify(e_geojson)