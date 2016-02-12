from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template
from model import (connect_to_db, db, User, Basket, Yarn, BasketYarn,
                   UserPreference, Preference, BasketYarnPhoto)
from jinja_filters import prettify_preference

app = Flask(__name__)
app.secret_key = "thatthingyouneedtoremembertodoitrhymeswithcount"
app.jinja_env.undefined = StrictUndefined

app.jinja_env.filters['prettify_preference'] = prettify_preference

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


@app.route("/")
def show_homepage():
    """Show the homepage of commuKNITty webapp"""

    return render_template("homepage.html")


@app.route("/profile/<int:user_id>")
def show_user_profile(user_id):
    """Show the user their info"""

    user = User.query.get(user_id)
    basket = Basket.query.filter(Basket.user_id == user.user_id).one()
    basket_yarns = BasketYarn.query.filter(BasketYarn.basket_id == basket.basket_id).all()

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
    user_pc = []
    user_weight = []
    user_pa = []
    user_fit = []

    # add pref_values to list for each category
    for pref in prefs:
        if pref.pref_category == "pc":
            user_pc.append(pref.pref_value)
        elif pref.pref_category == "weight":
            user_weight.append(pref.pref_value)
        elif pref.pref_category == "pa":
            user_pa.append(pref.pref_value)
        elif pref.pref_category == "fit":
            user_fit.append(pref.pref_value)

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

    return render_template("profile.html",
                           user=user,
                           basket_yarns=basket_yarns,
                           user_pc=user_pc,
                           user_weight=user_weight,
                           user_pa=user_pa,
                           user_fit=user_fit,
                           all_pc=all_pc,
                           all_weight=all_weight,
                           all_pa=all_pa,
                           all_fit=all_fit)


@app.route("/update_preference", methods=['POST'])
def update_preference_in_db(preference):
    """Process form field in user profile to update preferences.

    Updates database based on checkbox clicked"""





# TODO: search: build base request to include craft=knitting

# TODO: update user preferences: if they choose colorwork, should store all three:
#   intarsia, stranded, stripes-colorwork


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
