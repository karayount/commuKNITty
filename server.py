from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template, session, redirect, request, flash
from model import (connect_to_db, db, User, Basket, Yarn, BasketYarn,
                   UserPreference, Preference, BasketYarnPhoto)
from preferences import group_user_prefs, get_all_grouped_prefs
from jinja_filters import prettify_preference

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

    Updates database based on checkbox clicked. Include is 0 if checkbox
    empty, and 1 if checked. Preference sent to function is html ID, which
    is in format 'pref_category-pref_value'. """

    preference = request.form.get("preference")
    include = int(request.form.get("include"))

    # string parse preference so before first '-' is category and after is value
    index = preference.find('-')
    pref_category = preference[0:index]
    pref_value = preference[index+1:]

    # get preference object for this category-value pair, so pref_id can be used
    #   to add/remove UserPreference
    pref = Preference.query.filter(Preference.pref_category == pref_category,
                                   Preference.pref_value == pref_value).one()
    pref_id = pref.pref_id
    user_id = session["user_id"]

    if (include == 1):
        new_user_pref = UserPreference(user_id=user_id, pref_id=pref_id)
        db.session.add(new_user_pref)

    # if include == 0, search for record in db, and remove if there (it should be)
    else:
        user_pref_to_be_removed = UserPreference.query.filter(
            UserPreference.user_id == user_id,
            UserPreference.pref_id == pref_id).one()
        db.session.delete(user_pref_to_be_removed)

    db.session.commit()

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

    return render_template("search.html")


# TODO: search: build base request to include craft=knitting


@app.route("/yarn_driven_search/<int:basket_yarn_id>")
def yarn_driven_search(basket_yarn_id):
    """Shows patterns from API search given a basket yarn"""

    basket_yarn = BasketYarn.query.get(basket_yarn_id)
    yarn = Yarn.query.filter(Yarn.yarn_id == basket_yarn.yarn_id).first()

    base_url = "https://api.ravelry.com/patterns/search.json?sort=projects&craft=knitting"
    append_weight = "&weight="
    append_yardage = "&yardage=0%7C"
    append_page = "&page="

    if yarn != None:
        weight = yarn.yarn_weight
        yardage = basket_yarn.yards
        first_page = 1
        last_page = 10

        for i in range(first_page, last_page+1):
            search_url = base_url + append_weight + weight + append_yardage + yardage + append_page + str(i)

            page_of_patterns = requests.get(search_url)
            pattern_dict = page_of_patterns.json()
            patterns_fetched = pattern_dict.get("patterns", [])

            for pattern in patterns_fetched:
                permalink = pattern["permalink"]
                pattern_name = pattern["name"]
                pattern_id = pattern["id"]
                pattern_photo = pattern["first_photo"]["small_url"]

        # url_to_link http://www.ravelry.com/patterns/library/{{ pattern.permalink }}

        # show patterns with: image, name, pattern_category, link to Rav

    return "show results here"





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
