""" This module contains the functions to process searches"""

import requests



def build_pattern_list_from_yarn(basket_yarn_id):
    """ Returns list of patterns to make from input yarn.

    Searches for Projects with this Yarn, and collects pattern ids from
    those projects. Returns Pattern objects from those pattern ids.

    :param basket_yarn_id: primary key of BasketYarn
    :return: list of Pattern objects
    """

    basket_yarn = BasketYarn.query.get(basket_yarn_id)
    available_yards = basket_yarn.yards + 1

    pattern_ids_from_projects_with_this_yarn = (db.session.query(
        Project.project_rav_pattern_id).filter(
        Project.project_yarn_id == basket_yarn_id)).all()

    list_of_pattern_ids = []
    for pattern_id in pattern_ids_from_projects_with_this_yarn:
        list_of_pattern_ids.append(pattern_id[0])

    list_of_patterns = Pattern.query.filter(
        (Pattern.rav_pattern_id.in_(list_of_pattern_ids)) &
        (Pattern.req_yardage < available_yards) ).all()

    return list_of_patterns


def build_pattern_list_from_parameters(grouped_preferences):
    """ Returns list of patterns to make with input parameters.
    :param grouped_preferences: GroupedPreferences object
    :return: list of Pattern objects, based on input parameters
    """
    # build url with preferences
    # make API call
    # store results?
    # make results printable

    PREF_CATEGORIES = ["pc", "weight", "fit", "pa"]
    search_url = "https://api.ravelry.com/patterns/search.json?craft=knitting&sort=popularity"
    append_page = "&page="
    start_page = 1
    end_page = 5

    # add specific categories and values to search_url to customize
    for category in PREF_CATEGORIES:
        print category
        value_list = getattr(grouped_preferences, category)
        if len(value_list) == 0:
            continue
        search_url = search_url + "&" + category
        value_index = 0
        for value in value_list:
            if value_index == 0:
                search_url = search_url + "=" + value
            else:
                search_url = search_url + "%7C" + value
            value_index += 1

    # send get request to API for each page of results
    for page in range(start_page, end_page+1):
        search_url = search_url + append_page + str(page)
        page of patterns = requests.get(search_url)
