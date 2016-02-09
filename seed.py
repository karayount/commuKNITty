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


def load_yarns():
    """Load yarns into database from Ravelry API requests for most popular

       Ravelry pagination uses 50 records per page. Response in JSON."""

    base_request = "https://api.ravelry.com/yarns/search.json?sort=projects&page="

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
        for yarn in range(len(yarn_dict)):
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


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_yarns()
