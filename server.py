from jinja2 import StrictUndefined
from flask import Flask, render_template, session, redirect, request, flash, jsonify
from jinja_filters import prettify_preference
from model import connect_to_db, db, User, Basket, Yarn, BasketYarn, GroupEvent
from pattern_search import (build_pattern_list_from_parameters,
                            build_pattern_list_from_yarn,
                            build_short_pattern_list_from_parameters)
from preferences import (group_user_prefs, ALL_PREFERENCES,
                         update_user_preference, GroupedPreferences)
from local import get_businesses_from_yelp, create_map_markers


app = Flask(__name__)
app.secret_key = "thatthingyouneedtoremembertodoitrhymeswithcount"
app.jinja_env.undefined = StrictUndefined
app.jinja_env.filters['prettify_preference'] = prettify_preference


@app.route("/")
def show_landing_page():
    """Show the landing page of commuKNITty webapp"""

    return render_template("landing_page.html")


@app.route("/process_login", methods=["POST"])
def process_login():

    username = request.form.get("username")

    existing_user = User.query.filter(User.username == username).first()
    if existing_user is None:
        flash("Username incorrect. Please try logging in again.")
        return redirect("/")
    else:
        session["username"] = existing_user.username
        flash("Welcome, " + username)
        return redirect("/home")


@app.route("/process_logout")
def process_logout():

    del session["username"]

    flash("You're now logged out!")
    return redirect("/")


@app.route("/home")
def show_homepage():
    """Show homepage of logged in commuKNITty user"""

    logged_in_user = session.get("username")
    user = User.query.filter(User.username == logged_in_user).first()
    if user is None:
        flash("You are not authorized to view this page")
        return redirect("/")

    return render_template("homepage.html", user=user)


@app.route("/local")
def show_local():
    """ Show local page with Yelp map results and group meeting events.
    :return: rendered template
    """

    logged_in_user = session.get("username")
    user = User.query.filter(User.username == logged_in_user).first()
    if user is None:
        flash("You are not authorized to view this page")
        return redirect("/")

    business_list = get_businesses_from_yelp()
    group_events = GroupEvent.query.all()

    return render_template("local.html",
                           business_list=business_list,
                           groups=group_events)

# @app.route("/local")
# def test_mapbox():
#     """ Show local page with different mapbox config. Test.
#     :return: rendered template
#     """
#
#     logged_in_user = session.get("username", "")
#     user = User.query.filter(User.username == logged_in_user).first()
#     # verify that user is logged in
#     if user is None:
#         flash("You are not authorized to view this page")
#         return redirect("/")
#
#     business_list = get_businesses_from_yelp()
#     group_events = GroupEvent.query.all()
#
#     return render_template("zz-messing-with-things/test-mapbox.html",
#                            business_list=business_list,
#                            groups=group_events)


@app.route("/get_markers.json")
def get_markers():

    markers = create_map_markers()

    return jsonify(markers)

def verify_login(session):
    logged_in_user = session.get("username", "")
    user = User.query.filter(User.username == logged_in_user).first()
    # verify that user is logged in
    if user is None:
        flash("You are not authorized to view this page")
    return user

@app.route("/profile")
def show_user_profile():
    """Show the user their info"""
    #
    # logged_in_user = session.get("username", "")
    # user = User.query.filter(User.username == logged_in_user).first()
    # # verify that user is logged in
    # if user is None:
    #     flash("You are not authorized to view this page")
    #     return redirect("/")
    user = verify_login(session)
    if not user:
        return redirect("/")
    basket = Basket.query.filter(Basket.user_id == user.user_id).one()
    basket_yarns = BasketYarn.query.filter(BasketYarn.basket_id == basket.basket_id).all()

    # get GroupedPreferences object for user and all
    user_grouped_prefs = group_user_prefs(user)

    return render_template("profile.html",
                           user=user,
                           basket_yarns=basket_yarns,
                           user_prefs=user_grouped_prefs,
                           all_prefs=ALL_PREFERENCES)


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

    logged_in_user = session.get("username", "")
    user = User.query.filter(User.username == logged_in_user).first()
    # verify that user is logged in
    if user is None:
        flash("You are not authorized to view this page")
        return redirect("/")

    basket = Basket.query.filter(Basket.user_id == user.user_id).one()
    user_basket_yarns = BasketYarn.query.filter(BasketYarn.basket_id == basket.basket_id).all()

    return render_template("basket.html",
                           user=user,
                           user_basket_yarns=user_basket_yarns)


@app.route("/find_yarn_matches.json", methods=["POST"])
def find_yarn_matches():
    """ Takes in search string
    :return: JSON object with yarns matching search string
    """

    search_yarn = request.form.get("yarn_name")
    search_string = "%" + search_yarn + "%"

    yarn_list = Yarn.query.filter((Yarn.yarn_name.like(search_string))|
                                  (Yarn.yarn_company.like(search_string))).all()

    list_of_yarn_objs = []
    for yarn in yarn_list:
        current_yarn = {
            "yarn_id": yarn.yarn_id,
            "company": yarn.yarn_company,
            "yarn_name": yarn.yarn_name
        }
        list_of_yarn_objs.append(current_yarn)

    yarn_dict = {"yarns": list_of_yarn_objs}

    return jsonify(yarn_dict)


@app.route("/add_yarn_to_basket", methods=['POST'])
def add_yarn_to_basket():
    """ From new yarn entered by user, adds BasketYarn to database
    :return: redirects to /basket (will include newly added yarn)
    """

    logged_in_user = session.get("username", "")
    user = User.query.filter(User.username == logged_in_user).first()
    if user is None:
        flash("You are not authorized to view this page")
        return redirect("/")

    basket = Basket.query.filter(Basket.user_id == user.user_id).one()
    basket_id = basket.basket_id
    yarn_id = request.form.get("yarn_select")
    yards = request.form.get("yardage")
    colorway = request.form.get("colorway")

    new_basket_yarn = BasketYarn(basket_id=basket_id,
                                 yarn_id=yarn_id,
                                 yards=yards,
                                 colorway=colorway)

    db.session.add(new_basket_yarn)

    db.session.commit()

    return redirect("/basket")


@app.route("/search")
def show_search_page():
    """Search page for users: personalized recs, and for basket yarns."""

    logged_in_user = session.get("username", "")
    user = User.query.filter(User.username == logged_in_user).first()
    if user is None:
        flash("You are not authorized to view this page")
        return redirect("/")

    search_params = group_user_prefs(user)

    search_result_patterns = build_short_pattern_list_from_parameters(search_params)

    return render_template("search.html",
                           all_prefs=ALL_PREFERENCES,
                           pattern_recs=search_result_patterns)


@app.route("/yarn_driven_search/<int:basket_yarn_id>")
def yarn_driven_search(basket_yarn_id):
    """Shows patterns given a basket yarn.

    Patterns are linked to Yarns through Projects. This function will return
    Pattern object for which there are Projects which have both this Pattern
    and Yarn linked."""

    logged_in_user = session.get("username", "")
    user = User.query.filter(User.username == logged_in_user).first()
    if user is None:
        flash("You are not authorized to view this page")
        return redirect("/")

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

    logged_in_user = session.get("username", "")
    user = User.query.filter(User.username == logged_in_user).first()
    if user is None:
        flash("You are not authorized to view this page")
        return redirect("/")

    pc = request.form.getlist("pc")
    weight = request.form.getlist("weight")
    fit = request.form.getlist("fit")
    pa = request.form.getlist("pa")

    search_params = GroupedPreferences(pc, weight, fit, pa)

    patterns = build_pattern_list_from_parameters(search_params)
    headline = "Pattern results from your search"

    return render_template("pattern_search_results.html",
                           headline=headline,
                           patterns=patterns)


@app.route("/preference_search_results")
def show_preference_search_results():
    """ Shows patterns based on user preferences
    :return: html page with patterns
    """

    logged_in_user = session.get("username", "")
    user = User.query.filter(User.username == logged_in_user).first()
    if user is None:
        flash("You are not authorized to view this page")
        return redirect("/")

    search_params = group_user_prefs(user)

    search_result_patterns = build_pattern_list_from_parameters(search_params)
    headline = "Customized pattern recommendations for " + user.username

    return render_template("pattern_search_results.html",
                           patterns=search_result_patterns,
                           headline=headline)


if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    app.run()
