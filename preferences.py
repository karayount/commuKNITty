"""This module has helper functions to deal with Preferences"""

from model import UserPreference, Preference

# list mapping (pref_category, pref_value) pairs as tuples
ALL_PREFERENCES = [("weight", "lace"), ("weight", "fingering"),
                   ("weight", "sport"), ("weight", "dk"), ("weight", "worsted"),
                   ("weight", "aran"), ("weight", "bulky"), ("pc", "cardigan"),
                   ("pc", "pullover"), ("pc", "vest"), ("pc", "socks"),
                   ("pc", "mittens"), ("pc", "gloves"), ("pc", "fingerless"),
                   ("pc", "beanie-toque"), ("pc", "earflap"), ("pc", "cowl"),
                   ("pc", "scarf"), ("pc", "shawl-wrap"), ("fit", "adult"),
                   ("fit", "child"), ("fit", "baby"), ("pa", "cables"),
                   ("pa", "lace"), ("pa", "intarsia"), ("pa", "stranded"),
                   ("pa", "stripes-colorwork")]

def categorize_user_prefs(user):
    """ From input user, gather all preferences and categorize dictionary.

    Utilize join on UserPreference to access preferences.

    Returned dictionary has pref_category: pref_value pairs."""

    # get all of this user's preferences
    user_prefs = UserPreference.query.filter(UserPreference.user_id ==
                                             user.user_id).all()
    #loop through these to get associated preference objects
    prefs = []
    for user_pref in user_prefs:
        current_pref = Preference.query.filter(Preference.pref_id ==
                                               user_pref.pref_id).one()
        prefs.append(current_pref)

    # break user's preferences by category, group for printing on page
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


def categorize_all_prefs(all_preferences=ALL_PREFERENCES):
    """ Groups all possible preferences by category into dictionary.

    Returned dictionary has pref_category: pref_value pairs."""

    # break ALL_PREFERENCES up by category, group each
    all_pc = []
    all_weight = []
    all_pa = []
    all_fit = []

    # each pref tuple in ALL_PREFERENCES is (pref_category, pref_value)
    for pref in ALL_PREFERENCES:
        if pref[0] == "pc":
            all_pc.append(pref[1])
        elif pref[0] == "weight":
            all_weight.append(pref[1])
        elif pref[0] == "pa":
            all_pa.append(pref[1])
        elif pref[0] == "fit":
            all_fit.append(pref[1])

    categorized_prefs = {
        "all_pc": all_pc,
        "all_weight": all_weight,
        "all_pa": all_pa,
        "all_fit": all_fit
    }

    return categorized_prefs



