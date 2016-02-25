""" This module contains the functions to process searches"""

import requests
from model import BasketYarn, db, Project, Pattern
from preferences import ALL_PREFERENCES


class SearchResultPattern(object):
    """Pattern from API result, used for displaying search results."""

    def __init__(self, photo, name, rav_link):
        self.photo = photo
        self.name = name
        self.rav_link = rav_link


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
        Project.project_yarn_id == basket_yarn.yarn_id)).all()

    list_of_pattern_ids = []
    for pattern_id in pattern_ids_from_projects_with_this_yarn:
        list_of_pattern_ids.append(pattern_id[0])

    list_of_patterns = Pattern.query.filter(
        (Pattern.rav_pattern_id.in_(list_of_pattern_ids)) &
        (Pattern.req_yardage < available_yards) ).all()

    return list_of_patterns


def build_parameter_search_url(grouped_preferences):
    """ from GroupedPreferences (user or parameter), build url to search API
    :param grouped_preferences: GroupedPreferences object
    :return: url string
    """

    PREF_CATEGORIES = ["pc", "weight", "fit", "pa"]
    search_url = "https://api.ravelry.com/patterns/search.json?craft=knitting&photo=yes&availability=ravelry&sort=popularity"

    # add specific categories and values to search_url to customize
    for category in PREF_CATEGORIES:
        value_list = getattr(grouped_preferences, category)
        if ((len(value_list) == 0) and
                (category == "weight" or category == "pc")):
            value_list = getattr(ALL_PREFERENCES, category)
        search_url = search_url + "&" + category
        value_index = 0
        for value in value_list:
            if value_index == 0:
                search_url = search_url + "=" + value
            else:
                search_url = search_url + "|" + value
            value_index += 1
    return search_url


def search_patterns_from_ravelry(search_url):
    """ Searches Ravelry for patterns with given url, which includes params.
    :param search_url: url string for API request https://api.ravelry.com/patterns/search.json?craft=knitting&photo=yes&availability=ravelry&sort=popularity&pc=cardigan%7Cpullover%7Cvest%7Csocks%7Cmittens%7Cgloves%7Cfingerless%7Cbeanie-toque%7Cearflap%7Ccowl%7Cscarf%7Cshawl-wrap&weight=lace%7Cfingering%7Csport%7Cdk%7Cworsted%7Caran%7Cbulky&fit=adult%7Cchild%7Cbaby&pa=cables%7Clace%7Cintarsia%7Cstranded%7Cstripes-colorwork&page=1
    :return: list of SearchResultPattern objects
    """

    append_page = "&page="
    start_page = 1
    end_page = 1
    list_of_patterns = []

    for page in range(start_page, end_page+1):
        search_url = search_url + append_page + str(page)

        page_of_patterns = requests.get(search_url)
        # convert JSON to Python dictionary
        pattern_dict = page_of_patterns.json()
        pattern_list = pattern_dict["patterns"]

        for current_pattern in pattern_list:
            if ("first_photo" in current_pattern and
                "name" in current_pattern and "permalink" in current_pattern):
                if "small_url" in current_pattern["first_photo"]:
                    pattern_photo = current_pattern["first_photo"]["small_url"]
                    pattern_name = current_pattern["name"]
                    pattern_permalink = current_pattern["permalink"]
                    rav_pattern_link = ("http://www.ravelry.com/patterns/library/" +
                                            pattern_permalink)

                    new_pattern = SearchResultPattern(photo=pattern_photo,
                                                      name=pattern_name,
                                                      rav_link=rav_pattern_link)
                    list_of_patterns.append(new_pattern)
            else:
                print "skipped a pattern"

    return list_of_patterns


def build_pattern_list_from_parameters(grouped_preferences):
    """ Returns list of patterns to make with input parameters.
    :param grouped_preferences: GroupedPreferences object
    :return: list of SearchResultPattern objects, based on input parameters
    """

    search_url = build_parameter_search_url(grouped_preferences)

    list_of_patterns = search_patterns_from_ravelry(search_url)

    return list_of_patterns
