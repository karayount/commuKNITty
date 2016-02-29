"""Utility file to seed commuknitty database from Ravelry API calls, and
    from static data in files in seed_data/"""

from sqlalchemy import func
from model import (User, Preference, UserPreference, Basket, Yarn, BasketYarn,
                   GroupEvent, Project, Pattern)
from model import connect_to_db, db
from server import app
import requests
import csv


def load_users_and_create_baskets():
    """Load existing users into database from file"""

    print "Users"

    User.query.delete()
    user_data = "seed_data/user_data.txt"

    with open(user_data) as users:
        for row in users:
            row = row.rstrip()
            username, years_knitting, miles_knit, photo = row.split("|")

            # TODO: try except this
            if miles_knit != "":
                miles_knit = float(miles_knit)
            else:
                miles_knit = None

            user = User(username=username,
                        years_knitting=years_knitting,
                        miles_knit=miles_knit,
                        photo=photo)

            # Add new User object to the session
            db.session.add(user)
            db.session.flush()

            basket = Basket(user_id=user.user_id)
            db.session.add(basket)

        # Commit changes to DB
        db.session.commit()


def load_yarns():
    """Load yarns into database from Ravelry API requests for most popular

       Ravelry pagination uses 50 records per page. Response in JSON."""

    print "Yarns"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate records
    Yarn.query.delete()

    base_request = "https://api.ravelry.com/yarns/search.json?weight=lace%7Cfingering%7Csport%7Cdk%7Cworsted%7Caran%7Cbulky&sort=projects&page="

    # loop through first 40 pages (numbering starts at 1) to get 2000 records
    first_page = 1
    last_page = 40

    for i in range(first_page, last_page+1):
        # build request url using current page number
        current_page_request = base_request + str(i)
        # save response json for this page
        page_of_yarns = requests.get(current_page_request)
        # convert json to python dictionary
        yarn_dict = page_of_yarns.json()
        # python dictionary has 2 keys: paginator, and yarns (which is a list
        # of dictionaries, one per yarn object)
        yarns_fetched = yarn_dict.get("yarns", [])

        for yarn in yarns_fetched:

            rav_yarn_id = yarn["id"]
            # TODO: test if each one there (using get), use default or continue (if want to skip this one)
            yarn_name = yarn["name"]
            yarn_company = yarn["yarn_company_name"]
            yarn_weight = yarn["yarn_weight"]["name"]
            ball_yardage = yarn["yardage"]
            ball_grams = yarn["grams"]
            yarn_photo = yarn["first_photo"]["small_url"]
            yarn_permalink = yarn["permalink"]

            new_yarn = Yarn(rav_yarn_id=rav_yarn_id,
                            yarn_name=yarn_name,
                            yarn_company=yarn_company,
                            yarn_weight=yarn_weight,
                            ball_yardage=ball_yardage,
                            ball_grams=ball_grams,
                            yarn_photo=yarn_photo,
                            yarn_permalink=yarn_permalink)

            # Add new Yarn object to the session
            db.session.add(new_yarn)

        # Commit changes to DB
        db.session.commit()


def load_preferences():
    """Load all options for preferences, from file

       pref_category and pref_value will match Ravelry search terms,
       so they can be appended to url for API requests. Complete
       mapping is laid out in preferences.py """

    print "Preferences"

    Preference.query.delete()
    preference_data = "seed_data/preference_data.txt"

    with open(preference_data) as prefs:
        for row in prefs:
            row = row.rstrip()
            pref_id, pref_category, pref_value = row.split("|")

            pref_id = int(pref_id)

            preference = Preference(pref_id=pref_id,
                                    pref_category=pref_category,
                                    pref_value=pref_value)

            # Add new Preference object to the session
            db.session.add(preference)

        # Commit changes to DB
        db.session.commit()


def load_user_preferences():
    """Load user preferences from file"""

    print "UserPreferences"

    UserPreference.query.delete()
    user_preference_data = "seed_data/user_preference_data.txt"

    with open(user_preference_data) as user_prefs:
        for row in user_prefs:
            row = row.rstrip()
            user_id, pref_id = row.split("|")

            user_id = int(user_id)

            user_preference = UserPreference(user_id=user_id,
                                             pref_id=pref_id)

            # Add new UserPreference object to the session
            db.session.add(user_preference)

        # Commit changes to DB
        db.session.commit()


def load_basket_yarns():
    """Load BasketYarn data from file."""

    print "BasketYarns"

    BasketYarn.query.delete()
    basket_yarn_data = "seed_data/basket_yarn_data.txt"

    with open(basket_yarn_data) as basket_yarns:
        for row in basket_yarns:
            row = row.rstrip()
            basket_id, yarn_id, yards, colorway = row.split("|")

            basket_id = int(basket_id)
            yarn_id = int(yarn_id)
            yards = int(yards)

            basket_yarn = BasketYarn(basket_id=basket_id,
                                     yarn_id=yarn_id,
                                     yards=yards,
                                     colorway=colorway)

            # Add new BasketYarn object to the session
            db.session.add(basket_yarn)

        # Commit changes to DB
        db.session.commit()


def load_group_events():
    """ Load
    :return: none
    """

    group_event_data = "seed_data/group-events.csv"

    f = open(group_event_data)
    csv_f = csv.reader(f)

    for row in csv_f:
        group_name = row[0]
        day = row[1]
        time = row[2]
        location = row[3]
        city = row[4]

        group_event = GroupEvent(group_name=group_name,
                                 day=day,
                                 time=time,
                                 location=location,
                                 city=city)

        db.session.add(group_event)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_yarns()
    # load_users_and_create_baskets()
    # load_preferences()
    # load_user_preferences()
    # load_basket_yarns()
    # load_group_events()