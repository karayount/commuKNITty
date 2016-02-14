"""This module has helper functions to deal with Preferences"""

from model import UserPreference, Preference

# mapping of (pref_category, pref_value) pairs:
# ("weight", "lace"), ("weight", "fingering"), ("weight", "sport"),
# ("weight", "dk"), ("weight", "worsted"), ("weight", "aran"),
# ("weight", "bulky"), ("pc", "cardigan"), ("pc", "pullover"), ("pc", "vest"),
# ("pc", "socks"), ("pc", "mittens"), ("pc", "gloves"), ("pc", "fingerless"),
# ("pc", "beanie-toque"), ("pc", "earflap"), ("pc", "cowl"), ("pc", "scarf"),
# ("pc", "shawl-wrap"), ("fit", "adult"), ("fit", "child"), ("fit", "baby"),
# ("pa", "cables"), ("pa", "lace"), ("pa", "intarsia"), ("pa", "stranded"),
# ("pa", "stripes-colorwork")


class GroupedPreferences(object):
    """Attribute for each category which stores list of values."""

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

    categorized_user_prefs = {
        "pc": pc,
        "weight": weight,
        "pa": pa,
        "fit": fit
    }

    return categorized_user_prefs


def get_all_grouped_prefs():
    """ Returns GroupedPreferences object ALL_PREFERENCES"""

    return ALL_PREFERENCES



