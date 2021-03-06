"""This module has helper functions to deal with Preferences"""

from model import UserPreference, Preference, db, User
from flask import session


class GroupedPreferences(object):
    """Attribute for each category which stores list of values."""

    # pc and pa are ravelry category names, which will be used to build
    # urls to send API requests.
    def __init__(self, pc=[], weight=[], fit=[], pa=[]):
        self.pc = pc
        self.weight = weight
        self.fit = fit
        self.pa = pa


ALL_PREFERENCES = GroupedPreferences(weight=["lace", "fingering", "sport", "dk",
                                             "worsted", "aran", "bulky"],
                                     pc=["cardigan", "pullover", "vest",
                                         "socks", "mittens", "gloves",
                                         "fingerless", "beanie-toque",
                                         "earflap", "cowl", "scarf",
                                         "shawl-wrap"],
                                     fit=["adult", "child", "baby"],
                                     pa=["cables", "lace", "intarsia",
                                         "stranded", "stripes-colorwork"])


def group_user_prefs(user):
    """ From input user, gather preferences and create GroupedPreferences object.

    Utilize join on UserPreference to access preferences."""

    # get all of this user's preferences
    user_prefs = UserPreference.query.filter(UserPreference.user_id ==
                                             user.user_id).all()
    #loop through these UserPreferences to get associated preference objects
    prefs = []
    for user_pref in user_prefs:
        current_pref = Preference.query.filter(Preference.pref_id ==
                                               user_pref.pref_id).one()
        prefs.append(current_pref)

    # break user's preferences into lists by category
    pc = []
    weight = []
    pa = []
    fit = []

    # add pref_values to list for each category
    for pref in prefs:
        if pref.pref_category == "pc":
            pc.append(pref.pref_value)
        elif pref.pref_category == "weight":
            weight.append(pref.pref_value)
        elif pref.pref_category == "pa":
            pa.append(pref.pref_value)
        elif pref.pref_category == "fit":
            fit.append(pref.pref_value)

    categorized_user_prefs = GroupedPreferences(weight=weight,
                                                pc=pc,
                                                fit=fit,
                                                pa=pa)

    return categorized_user_prefs


def update_user_preference(preference, include):
    """ Takes id of changed checkbox and updates user_preferences table.

    :param preference: html ID of checkbox, as 'pref_category-pref_value'.
    :param include: 0 or 1 to indicate whether checkbox is checked
    :return: None
    """

    # string parse preference so before first '-' is category and after is value
    index = preference.find('-')
    pref_category = preference[0:index]
    pref_value = preference[index+1:]

    # get preference object for this category-value pair, so pref_id can be used
    #   to add/remove UserPreference
    pref = Preference.query.filter(Preference.pref_category == pref_category,
                                   Preference.pref_value == pref_value).one()
    pref_id = pref.pref_id
    user = User.query.filter(User.username == session.get("username")).first()
    user_id = user.user_id

    if (include == 1):
        new_user_pref = UserPreference(user_id=user_id, pref_id=pref_id)
        db.session.add(new_user_pref)

    # if include == 0, search for record in db, and remove if there (should be)
    else:
        user_pref_to_be_removed = UserPreference.query.filter(
            UserPreference.user_id == user_id,
            UserPreference.pref_id == pref_id).one()
        db.session.delete(user_pref_to_be_removed)

    db.session.commit()


