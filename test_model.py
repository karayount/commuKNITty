
from model import (connect_to_db, db, User, UserPreference,
                   GroupEvent, Preference, Basket, Yarn, BasketYarn, Project,
                   Pattern)


def create_example_data():
    """ create sample data for testing.
    :return: created data in database
    """

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Preference.query.delete()
    Yarn.query.delete()
    BasketYarn.query.delete()
    Project.query.delete()
    Pattern.query.delete()

    # Add users
    u1 = User(username="u1", years_knitting=6, miles_knit=23)
    u2 = User(username="u2", years_knitting=2)
    u3 = User(username="u3")
    # flush users since Basket is dependent
    db.session.add_all([u1, u2, u3])
    db.session.flush()
    b1 = Basket(user_id=1)
    b2 = Basket(user_id=2)
    b3 = Basket(user_id=3)
    y1 = Yarn(rav_yarn_id=1, yarn_name="y1", yarn_company="y1_company",
              yarn_weight="y1_weight", ball_yardage=100,
              yarn_photo="y1_photo", yarn_permalink="y1_permalink")
    y2 = Yarn(rav_yarn_id=2, yarn_name="y2", yarn_company="y2_company",
          yarn_weight="y2_weight", ball_yardage=200,
          yarn_photo="y2_photo", yarn_permalink="y2_permalink")
    y3 = Yarn(rav_yarn_id=3, yarn_name="y3", yarn_company="y3_company",
          yarn_weight="y3_weight", ball_yardage=300,
          yarn_photo="y3_photo", yarn_permalink="y3_permalink")
    # flush baskets and yarns since BasketYarn is dependent
    db.session.add_all([b1, b2, b3, y1, y2, y3])
    db.session.flush()
    by1 = BasketYarn(basket_id=1, yarn_id=1, yards=1000, colorway="by1_color")
    by2 = BasketYarn(basket_id=1, yarn_id=2, yards=1000, colorway="by2_color")
    by3 = BasketYarn(basket_id=1, yarn_id=3, yards=1000, colorway="by3_color")
    by4 = BasketYarn(basket_id=2, yarn_id=1, yards=1000, colorway="by4_color")
    by5 = BasketYarn(basket_id=2, yarn_id=2, yards=1000, colorway="by5_color")
    by6 = BasketYarn(basket_id=2, yarn_id=3, yards=1000, colorway="by6_color")
    by7 = BasketYarn(basket_id=3, yarn_id=1, yards=1000, colorway="by7_color")
    by8 = BasketYarn(basket_id=3, yarn_id=2, yards=1000, colorway="by8_color")
    by9 = BasketYarn(basket_id=3, yarn_id=3, yards=1000, colorway="by9_color")
    # add projects and patterns
    pr1 = Project(project_yarn_id=1, project_rav_pattern_id=1,
                  project_pattern_name="pr1_name",
                  project_yarn_permalink="pr1_permalink")
    pr2 = Project(project_yarn_id=1, project_rav_pattern_id=2,
                  project_pattern_name="pr1_name",
                  project_yarn_permalink="pr2_permalink")
    pr3 = Project(project_yarn_id=1, project_rav_pattern_id=3,
                  project_pattern_name="pr3_name",
                  project_yarn_permalink="pr3_permalink")
    pr4 = Project(project_yarn_id=1, project_rav_pattern_id=4,
                  project_pattern_name="pr4_name",
                  project_yarn_permalink="pr5_permalink")
    pr5 = Project(project_yarn_id=1, project_rav_pattern_id=5,
                  project_pattern_name="pr5_name",
                  project_yarn_permalink="pr5_permalink")
    pr6 = Project(project_yarn_id=2, project_rav_pattern_id=3,
                  project_pattern_name="pr6_name",
                  project_yarn_permalink="pr6_permalink")
    pr7 = Project(project_yarn_id=2, project_rav_pattern_id=4,
                  project_pattern_name="pr7_name",
                  project_yarn_permalink="pr7_permalink")
    pr8 = Project(project_yarn_id=2, project_rav_pattern_id=5,
                  project_pattern_name="pr8_name",
                  project_yarn_permalink="pr8_permalink")
    pr9 = Project(project_yarn_id=2, project_rav_pattern_id=6,
                  project_pattern_name="pr9_name",
                  project_yarn_permalink="pr9_permalink")
    pr10 = Project(project_yarn_id=2, project_rav_pattern_id=7,
                   project_pattern_name="pr10_name",
                   project_yarn_permalink="pr10_permalink")
    pr11 = Project(project_yarn_id=3, project_rav_pattern_id=5,
                   project_pattern_name="pr11_name",
                   project_yarn_permalink="pr11_permalink")
    pr12 = Project(project_yarn_id=3, project_rav_pattern_id=6,
                   project_pattern_name="pr12_name",
                   project_yarn_permalink="pr12_permalink")
    pr13 = Project(project_yarn_id=3, project_rav_pattern_id=7,
                   project_pattern_name="pr13_name",
                   project_yarn_permalink="pr13_permalink")
    pr14 = Project(project_yarn_id=3, project_rav_pattern_id=8,
                   project_pattern_name="pr14_name",
                   project_yarn_permalink="pr14_permalink")
    pr15 = Project(project_yarn_id=3, project_rav_pattern_id=9,
                   project_pattern_name="pr15_name",
                   project_yarn_permalink="pr15_permalink")
    pa1 = Pattern(rav_pattern_id=1, pattern_photo="pa1_photo", req_yardage=100,
                  pattern_yarn_weight="y1_weight", pattern_name="pa1_name",
                  pattern_category="cardigan", rav_pattern_link="pa1_link")
    pa2 = Pattern(rav_pattern_id=2, pattern_photo="pa2_photo", req_yardage=200,
                  pattern_yarn_weight="y2_weight", pattern_name="pa2_name",
                  pattern_category="pullover", rav_pattern_link="pa2_link")
    pa3 = Pattern(rav_pattern_id=3, pattern_photo="pa3_photo", req_yardage=300,
                  pattern_yarn_weight="y3_weight", pattern_name="pa3_name",
                  pattern_category="socks", rav_pattern_link="pa3_link")
    pa4 = Pattern(rav_pattern_id=4, pattern_photo="pa4_photo", req_yardage=400,
                  pattern_yarn_weight="y4_weight", pattern_name="pa4_name",
                  pattern_category="mittens", rav_pattern_link="pa4_link")
    pa5 = Pattern(rav_pattern_id=5, pattern_photo="pa5_photo", req_yardage=500,
                  pattern_yarn_weight="y5_weight", pattern_name="pa5_name",
                  pattern_category="gloves", rav_pattern_link="pa5_link")
    pa6 = Pattern(rav_pattern_id=6, pattern_photo="pa6_photo", req_yardage=600,
                  pattern_yarn_weight="y6_weight", pattern_name="pa6_name",
                  pattern_category="beanie-toque", rav_pattern_link="pa6_link")
    pa7 = Pattern(rav_pattern_id=7, pattern_photo="pa7_photo", req_yardage=700,
                  pattern_yarn_weight="y7_weight", pattern_name="pa7_name",
                  pattern_category="cowl", rav_pattern_link="pa7_link")
    pa8 = Pattern(rav_pattern_id=8, pattern_photo="pa8_photo", req_yardage=800,
                  pattern_yarn_weight="y8_weight", pattern_name="pa8_name",
                  pattern_category="scarf", rav_pattern_link="pa8_link")
    pa9 = Pattern(rav_pattern_id=9, pattern_photo="pa9_photo", req_yardage=900,
                  pattern_yarn_weight="y9_weight", pattern_name="pa9_name",
                  pattern_category="shawl-wrap", rav_pattern_link="pa9_link")

    db.session.add_all([by1, by2, by3, by4, by5, by6, by7, by8, by9,])
    db.session.add_all([pr1, pr2, pr3, pr4, pr5, pr6, pr7, pr8, pr9, pr10, pr11, pr12, pr13, pr14, pr15])
    db.session.add_all([pa1, pa2, pa3, pa4, pa5, pa6, pa7, pa8, pa9])
    db.session.commit()
