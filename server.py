from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template, session, redirect, request, flash
from model import (connect_to_db, db, User, Basket, Yarn, BasketYarn,
                   UserPreference, Preference, BasketYarnPhoto)
from preferences import categorize_user_prefs, categorize_all_prefs
from jinja_filters import prettify_preference

app = Flask(__name__)
app.secret_key = "thatthingyouneedtoremembertodoitrhymeswithcount"
app.jinja_env.undefined = StrictUndefined

app.jinja_env.filters['prettify_preference'] = prettify_preference


@app.route("/")
def show_landing_page():
    """Show the landing page of commuKNITty webapp"""

    return render_template("landing_page.html")


@app.route("/home")
def show_homepage():
    """Show homepage of logged in commuKNITty user"""

    return render_template("homepage.html")


@app.route("/process_login")
def process_login():

    username = request.form.get("username")

    existing_user = User.query.filter(User.username == username).first()
    if existing_user is None:
        flash("Username incorrect. Please re-enter")
        return redirect("/")
    else:
        session["user"] = existing_user
        return redirect("/home")


@app.route("/profile/<int:user_id>")
def show_user_profile(user_id):
    """Show the user their info"""

    user = User.query.get(user_id)
    basket = Basket.query.filter(Basket.user_id == user.user_id).one()
    basket_yarns = BasketYarn.query.filter(BasketYarn.basket_id == basket.basket_id).all()

    # get dictionary of categorizes user preferences
    user_prefs = categorize_user_prefs(user)
    # create lists to pass to jinja
    user_pc = user_prefs["pc"]
    user_weight = user_prefs["weight"]
    user_pa = user_prefs["pa"]
    user_fit = user_prefs["fit"]

    all_prefs = categorize_all_prefs()
    # create list to pass to jinja
    all_pc = all_prefs["all_pc"]
    all_weight = all_prefs["all_weight"]
    all_pa = all_prefs["all_pa"]
    all_fit = all_prefs["all_fit"]

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


@app.route("/basket")
def show_basket():
    """Shows yarns in user's basket"""

    # basket = Basket.query.filter(basket.user_id == user.user_id)


# TODO: search: build base request to include craft=knitting

# TODO: update user preferences: if they choose colorwork, should store all three:
#   intarsia, stranded, stripes-colorwork


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
