import json

from model import Yarn, db, Project, Pattern
import requests

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

        for page in range(1, 11):
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

                    db.session.add(new_project)
                except UnicodeEncodeError:
                    continue

    db.session.commit()


get_project_from_yarns(1, 5)


# the search below has ~2 million results
# http://www.ravelry.com/projects/search#weight=lace%7Cfingering%7Csport%7Cdk%7Cworsted%7Caran%7Cbulky&pc=cardigan%7Cpullover%7Cvest%7Csocks%7Cfingerless%7Cgloves%7Cmittens%7Cbeanie-toque%7Cearflap%7Cscarf%7Cshawl-wrap%7Ccowl&sort=best&yardage=0%7C2000&status=finished&view=cards&craft=knitting&ravelry-download=yes
