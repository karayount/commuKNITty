from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template, session, redirect, request, flash
from jinja_filters import prettify_preference

from model import (connect_to_db, db, User, Basket, Yarn, BasketYarn,
                   UserPreference, Preference, BasketYarnPhoto, Project,
                   Pattern)
from preferences import (group_user_prefs, get_all_grouped_prefs,
                         update_user_preference, GroupedPreferences)
from search import (build_pattern_list_from_parameters,
                    build_pattern_list_from_yarn)

app = Flask(__name__)
app.secret_key = "thatthingyouneedtoremembertodoitrhymeswithcount"
app.jinja_env.undefined = StrictUndefined

app.jinja_env.filters['prettify_preference'] = prettify_preference


@app.route("/")
def show_landing_page():
    """Show the landing page of commuKNITty webapp"""

    return render_template("landing_page.html")


@app.route("/process_login")
def process_login():

    username = request.args.get("username")

    existing_user = User.query.filter(User.username == username).first()
    if existing_user is None:
        flash("Username incorrect. Please re-enter")
        return redirect("/")
    else:
        session["user_id"] = existing_user.user_id
        return redirect("/home")

@app.route("/home")
def show_homepage():
    """Show homepage of logged in commuKNITty user"""

    user = User.query.get(session["user_id"])


    return render_template("homepage.html", user=user)

@app.route("/profile/<int:user_id>")
def show_user_profile(user_id):
    """Show the user their info"""

    user = User.query.get(user_id)
    basket = Basket.query.filter(Basket.user_id == user.user_id).one()
    basket_yarns = BasketYarn.query.filter(BasketYarn.basket_id == basket.basket_id).all()

    # get GroupedPreferences object for user and all
    user_grouped_prefs = group_user_prefs(user)
    all_grouped_prefs = get_all_grouped_prefs()

    return render_template("profile.html",
                           user=user,
                           basket_yarns=basket_yarns,
                           user_prefs=user_grouped_prefs,
                           all_prefs=all_grouped_prefs)


@app.route("/update_preference.json", methods=['POST'])
def update_preference_in_db():
    """Process form field in user profile to update preferences.

    calls update_user_preference to update database based on checkbox clicked.
    Include is 0 if checkbox empty, and 1 if checked.
    Preference sent to function is html ID, which is in format
    'pref_category-pref_value'. """

    preference = request.form.get("preference")
    include = int(request.form.get("include"))

    # update the db to reflect the change in user preference
    update_user_preference(preference, include)

    display_id = preference + "-display"

    return display_id


@app.route("/basket")
def show_basket():
    """Shows yarns in user's basket"""

    user = User.query.get(session["user_id"])
    basket = Basket.query.filter(Basket.user_id == user.user_id).one()
    user_basket_yarns = BasketYarn.query.filter(BasketYarn.basket_id == basket.basket_id).all()

    return render_template("basket.html",
                           user=user,
                           user_basket_yarns=user_basket_yarns)


@app.route("/search")
def show_search_page():
    """Search page for users: personalized recs, and for basket yarns."""

    all_grouped_prefs = get_all_grouped_prefs()

    return render_template("search.html",
                           all_prefs=all_grouped_prefs)


# TODO: search: build base request to include craft=knitting


@app.route("/yarn_driven_search/<int:basket_yarn_id>")
def yarn_driven_search(basket_yarn_id):
    """Shows patterns given a basket yarn.

    Patterns are linked to Yarns through Projects. This function will return
    Pattern object for which there are Projects which have both this Pattern
    and Yarn linked."""

    basket_yarn = BasketYarn.query.get(basket_yarn_id)
    list_of_patterns = build_pattern_list_from_yarn(basket_yarn_id)

    return render_template("patterns_for_basket_yarn.html",
                           basket_yarn=basket_yarn,
                           patterns=list_of_patterns)


@app.route("/parameter_search_results", methods=['POST'])
def show_parameter_search_results():
    """ Shows patterns based on user selections
    :return: html page with patterns
    """

    pc = request.form.getlist("pc")
    weight = request.form.getlist("weight")
    fit = request.form.getlist("fit")
    pa = request.form.getlist("pa")

    search_params = GroupedPreferences(pc, weight, fit, pa)

    patterns = build_pattern_list_from_parameters(search_params)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
