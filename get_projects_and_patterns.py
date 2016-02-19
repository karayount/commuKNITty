""" This script loads Project and Pattern objects into db from API calls
to Ravelry. It is intended to be run a single time.
"""

import json

from model import Yarn, db, Project, Pattern
import requests
from preferences import ALL_PREFERENCES


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///commuknitty'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."


def get_project_from_yarns(start_index, end_index):
    """ Create Project objects for Ravelry projects made with yarn in db.

    This function should be called so that db is seeded with Projects
    associated with each of the 2000 Yarns.

    :param start_index: first yarn to get projects for
    :param end_index: last yarn to get projects for
    :return: None
    """

    # there are 2000 of these, since there are 2000 Yarn objects in database
    yarns_to_search = db.session.query(Yarn.yarn_id, Yarn.yarn_permalink).all()


    base_search = "https://api.ravelry.com/projects/search.json?sort=favorites&photo=yes&craft=knitting&status=finished&yardage=0%7C2000&ravelry-download=yes&query="
    append_categories = "&pc=cardigan%7Cpullover%7Cvest%7Csocks%7Cfingerless%7Cgloves%7Cmittens%7Cbeanie-toque%7Cearflap%7Cscarf%7Cshawl-wrap%7Ccowl"
    append_page = "&page="

    for i in range(start_index, end_index+1):
        yarn_id, yarn_permalink = yarns_to_search[i]
        yarn_pattern_ids = set([])

        for page in range(1, 6):
            # create url for API request
            search_string = (base_search + yarn_permalink + append_categories +
                             append_page + str(page))
            # get json response from API call
            json_projects_from_yarn = requests.get(search_string)

            # convert json to python dictionary
            dict_projects_from_yarn = json_projects_from_yarn.json()
            # pull out list of projects from dictionary, or empty list
            projects_from_yarn = dict_projects_from_yarn.get("projects", [])
            #loop through list of projects to create new Project objects
            for project in projects_from_yarn:
                project_rav_pattern_id = project.get("pattern_id", "")
                project_pattern_name = project.get("pattern_name", "")

                # exclude projects missing pattern id or pattern name
                if project_rav_pattern_id == "" or project_pattern_name == "":
                    continue
                # exclude projects where pattern already paired with yarn
                if project_rav_pattern_id in yarn_pattern_ids:
                    continue
                else:
                    yarn_pattern_ids.add(project_rav_pattern_id)

                try:
                    new_project = Project(project_yarn_id = yarn_id,
                                          project_yarn_permalink = yarn_permalink,
                                          project_rav_pattern_id = project_rav_pattern_id,
                                          project_pattern_name = project_pattern_name)
                    print i, page, project_pattern_name
                    db.session.add(new_project)
                except UnicodeEncodeError:
                    continue

            db.session.commit()


def get_patterns_from_projects(start_index, end_index):
    """ Using Projects, create Pattern objects.

    Use Ravelry API to retrieve patterns with pattern_name from Project.
    Compare retrieved pattern pattern_ids to pattern_id in Project, and
    create Pattern object for matches."""

    patterns_to_find = db.session.query(Project.project_rav_pattern_id).all()
    # remove duplicates by transforming list into set, then back
    patterns_to_find = set(patterns_to_find)
    patterns_to_find = list(patterns_to_find)
    # 41468 (from 251081 in initial list)

    base_url = "https://api.ravelry.com/patterns/"
    append_extension = ".json"

    for i in range(start_index, end_index+1):
        project_rav_pattern_id = patterns_to_find[i][0]
        search_string = base_url + str(project_rav_pattern_id) + append_extension
        # submit search through get request to Ravelry API
        json_pattern = requests.get(search_string)
        # convert json to python dictionary
        dict_project_pattern = json_pattern.json()
        current_pattern = dict_project_pattern["pattern"]

        # save information from dictionary, if any is missing, don't add
        # this pattern to database
        try:
            pattern_photo = current_pattern["photos"][0]["small_url"]
            req_yardage = current_pattern["yardage_max"]
            if req_yardage == None:
                req_yardage = current_pattern["yardage"]
                if req_yardage == None:
                    continue
            try:
                pattern_yarn_weight = current_pattern["yarn_weight"]["name"]
            except KeyError:
                if current_pattern["packs"][0]["yarn_weight"] == None:
                    continue
                else:
                    pattern_yarn_weight = current_pattern["packs"][0]["yarn_weight"]["name"]
            pattern_name = current_pattern["name"]
            pattern_permalink = current_pattern["permalink"]
            pattern_categories = current_pattern["pattern_categories"]
        except (KeyError, IndexError):
            continue

        # build variables from json data to create object
        pattern_yarn_weight = pattern_yarn_weight.lower()
        if pattern_yarn_weight not in (ALL_PREFERENCES.weight):
            continue
        rav_pattern_link = ("http://www.ravelry.com/patterns/library/" +
                            pattern_permalink)
        try:
            for category in pattern_categories:
                if category["permalink"] in (ALL_PREFERENCES.pc):
                    pattern_category = category["permalink"]
                elif (category["parent"]["permalink"] == "socks"):
                    pattern_category = "socks"
                else:
                    continue
        except KeyError:
            continue

        # create new Pattern object and save it to db
        new_pattern = Pattern(rav_pattern_id=project_rav_pattern_id,
                              pattern_photo=pattern_photo,
                              req_yardage=req_yardage,
                              pattern_yarn_weight=pattern_yarn_weight,
                              pattern_name=pattern_name,
                              pattern_category=pattern_category,
                              rav_pattern_link=rav_pattern_link)

        db.session.add(new_pattern)
        print i

    db.session.commit()


# get_patterns_from_projects(0, 10)
# get_patterns_from_projects(11, 30)
# get_patterns_from_projects(31, 100)
# get_patterns_from_projects(101, 150)
# get_patterns_from_projects(151, 400)
# get_patterns_from_projects(401, 1000)
# get_patterns_from_projects(1001, 1883)
# get_patterns_from_projects(1884, 1884)
# get_patterns_from_projects(1884, 2000)
# get_patterns_from_projects(2001, 3000)
# get_patterns_from_projects(3001, 5000)
# get_patterns_from_projects(5001, 5500)
# get_patterns_from_projects(5501, 7000)
# get_patterns_from_projects(7001, 10000)
# get_patterns_from_projects(10001, 16321)
# get_patterns_from_projects(16322, 16322)
# get_patterns_from_projects(16323, 16405)
# get_patterns_from_projects(16406, 17000)
# get_patterns_from_projects(17001, 20000)
# get_patterns_from_projects(20001, 25000)
# get_patterns_from_projects(25001, 41466)
get_patterns_from_projects(41467,41467)


#41468





# get_project_from_yarns(1998, 1999)
# get_project_from_yarns(1990, 1997)
# get_project_from_yarns(1970, 1989)
# get_project_from_yarns(1940, 1969)
# get_project_from_yarns(1900, 1939)
# get_project_from_yarns(1800, 1899)
# get_project_from_yarns(1700, 1799)
# get_project_from_yarns(1500, 1699)
# get_project_from_yarns(1300, 1499)
# get_project_from_yarns(1000, 1299)
# get_project_from_yarns(500, 999)
# get_project_from_yarns(400, 499)
# get_project_from_yarns(200, 399)
# get_project_from_yarns(0, 199)
