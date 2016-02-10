from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template
from model import connect_to_db, db, User, Basket, Yarn, BasketYarn, Preference
from jinja_filters import prettify_preference

app = Flask(__name__)
app.secret_key = "thatthingyouneedtoremembertodoitrhymeswithcount"
app.jinja_env.undefined = StrictUndefined

app.jinja_env.filters['prettify_preference'] = prettify_preference


@app.route("/")
def show_homepage():
    """Show the homepage of commuKNITty webapp"""

    return render_template("homepage.html")


@app.route("/profile/<int:user_id>")
def show_user_profile(user_id):
    """Show the user their info"""

    # show some photos with link to basket
    # show preferences
    # allow to add/update preferences
    user = User.query.get(user_id)
    basket = Basket.query.filter(Basket.user_id == user.user_id).one()
    basket_yarns = BasketYarn.query.filter(BasketYarn.basket_id == basket.basket_id).all()
    pc = Preference.query.filter(Preference.user_id == user.user_id,
                                 Preference.pref_category == "pc").all()
    weight = Preference.query.filter(Preference.user_id == user.user_id,
                                     Preference.pref_category == "weight").all()
    pa = Preference.query.filter(Preference.user_id == user.user_id,
                                 Preference.pref_category == "pa").all()
    fit = Preference.query.filter(Preference.user_id == user.user_id,
                                  Preference.pref_category == "fit").all()

    return render_template("profile.html",
                           user=user,
                           basket_yarns=basket_yarns,
                           pc=pc,
                           weight=weight,
                           pa=pa,
                           fit=fit)


# search: build base request to include craft=knitting

# update user preferences: if they choose colorwork, should store all three:
#   intarsia, stranded, stripes-colorwork


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
