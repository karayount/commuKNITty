"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Preference
from model import Basket
from model import Yarn
from model import BasketYarn
from model import BasketYarnPhoto

from model import connect_to_db, db
from server import app
import requests


def load_users_and_create_baskets():
    """Load existing users into database from file"""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate records
    User.query.delete()

    for row in open("seed_data/user_data.txt"):
        row = row.rstrip()
        username, years_knitting, miles_knit, photo = row.split("|")

        if miles_knit != "":
            miles_knit = float(miles_knit)
        else:
            miles_knit = None

        user = User(username=username,
                    years_knitting=years_knitting,
                    miles_knit=miles_knit,
                    photo=photo)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)
        db.session.flush()

        basket = Basket(user_id=user.user_id)
        db.session.add(basket)

    # Once we're done, we should commit our work
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
    for i in range(1, 41):
        # build request url using current page number
        current_page_request = base_request + str(i)
        # save response json for this page
        page_of_yarns = requests.get(current_page_request)
        # convert json to python dictionary
        yarn_dict = page_of_yarns.json()
        # python dictionary has 2 keys: paginator, and yarns (which is a list
        # of dictionaries, one per yarn object)
        print i
        print len(yarn_dict["yarns"])
        for yarn in range(len(yarn_dict["yarns"])):
            rav_yarn_id = yarn_dict["yarns"][yarn]["id"]
            yarn_name = yarn_dict["yarns"][yarn]["name"]
            yarn_company = yarn_dict["yarns"][yarn]["yarn_company_name"]
            yarn_weight = yarn_dict["yarns"][yarn]["yarn_weight"]["name"]
            ball_yardage = yarn_dict["yarns"][yarn]["yardage"]
            ball_grams = yarn_dict["yarns"][yarn]["grams"]

            new_yarn = Yarn(rav_yarn_id=rav_yarn_id,
                            yarn_name=yarn_name,
                            yarn_company=yarn_company,
                            yarn_weight=yarn_weight,
                            ball_yardage=ball_yardage,
                            ball_grams=ball_grams)

            # print new_yarn

            # We need to add to the session or it won't ever be stored
            db.session.add(new_yarn)

        # Once we're done, we should commit our work
        db.session.commit()


def load_preferences():
    """Load user preferences from file

       pref_category will and pref_value will match Ravelry search terms,
       so they can be appended to url for API requests. "pc" stands for
       pattern category, and "pa" is pattern attribute.

       Mapping is as follows "pref_category: pref_value"
       weight: lace, weight: fingering, weight: sport, weight: dk,
       weight: worsted, weight: aran, weight: bulky, pc: cardigan,
       pc: pullover, pc: vest, pc: socks, pc: mittens, pc: gloves,
       pc: fingerless, pc: beanie-toque, pc: earflap, pc: cowl,
       pc: scarf, pc: shawl-wrap, fit: adult, fit: child, fit: baby,
       pa: cables, pa: lace, pa: intarsia, pa: stranded, pa: stripes-colorwork
       """

    print "Preferences"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate records
    Preference.query.delete()

    for row in open("seed_data/preference_data.txt"):
        row = row.rstrip()
        user_id, pref_category, pref_value = row.split("|")

        user_id = int(user_id)

        preference = Preference(user_id=user_id,
                                pref_category=pref_category,
                                pref_value=pref_value)

        # We need to add to the session or it won't ever be stored
        db.session.add(preference)

    # Once we're done, we should commit our work
    db.session.commit()


def load_basket_yarns():
    """Load BasketYarn data from file."""

    print "BasketYarns"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate records
    BasketYarn.query.delete()

    for row in open("seed_data/basket_yarns.txt"):
        row = row.rstrip()
        basket_id, yarn_id, yards, colorway = row.split("|")

        basket_id = int(basket_id)
        yarn_id = int(yarn_id)
        yards = int(yards)

        basket_yarn = BasketYarn(basket_id=basket_id,
                                 yarn_id=yarn_id,
                                 yards=yards,
                                 colorway=colorway)

        # We need to add to the session or it won't ever be stored
        db.session.add(basket_yarn)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_yarns()
    load_users_and_create_baskets()
    load_preferences()
    load_basket_yarns()
