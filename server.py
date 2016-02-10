from jinja2 import StrictUndefined
import requests
from flask import Flask, render_template
from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = "thatthingyouneedtoremembertodoitrhymeswithcount"
app.jinja_env.undefined = StrictUndefined


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

    return render_template("profile.html")  # include user object, so can display username)


# search: build base request to include craft=knitting


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.run()
