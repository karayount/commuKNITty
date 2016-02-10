"""Models and database functions for commuKNITty webapp"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class User(db.Model):
    """User of commuKNITty webapp"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    years_knitting = db.Column(db.String(40))
    miles_knit = db.Column(db.Float)
    photo = db.Column(db.String(400))

    preferences = db.relationship("Preference")
    basket = db.relationship("Basket")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s>" % (self.user_id, self.username)


class Preference(db.Model):
    """Preference of commuKNITty app User"""

    __tablename__ = "preferences"

    pref_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    # pref_category, pref_value will be used for Ravelry API search parameters
    pref_category = db.Column(db.String(50), nullable=False)
    pref_value = db.Column(db.String(50), nullable=False)

    user = db.relationship("User")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Preference pref_id=%s category=%s>" % (self.pref_id,
                                                        self.pref_category)


class Basket(db.Model):
    """Basket of Yarns belonging to commuKNITty User."""

    __tablename__ = "baskets"

    basket_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    user = db.relationship("User")
    yarns = db.relationship("BasketYarn")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Basket basket_id=%s user_id=%s>" % (self.basket_id, self.user_id)


class Yarn(db.Model):
    """Yarn line from brand, with per-ball properties"""

    __tablename__ = "yarns"

    yarn_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # rav_yarn_id is ravelry's key for this record, to simplify searching
    rav_yarn_id = db.Column(db.Integer)
    # attributes below will be copied from ravelry, for simpler search
    yarn_name = db.Column(db.String(100))
    yarn_company = db.Column(db.String(50))
    yarn_weight = db.Column(db.String(25))
    ball_yardage = db.Column(db.Integer)
    ball_grams = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Yarn yarn_id=%s yarn_name=%s>" % (self.yarn_id, self.yarn_name)


class BasketYarn(db.Model):
    """Yarn in basket of a User of commuKNITty webapp"""

    __tablename__ = "basket_yarns"

    basket_yarn_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    basket_id = db.Column(db.Integer,
                          db.ForeignKey('baskets.basket_id'),
                          nullable=False)
    yarn_id = db.Column(db.Integer,
                        db.ForeignKey('yarns.yarn_id'),
                        nullable=False)
    yards = db.Column(db.Integer)
    colorway = db.Column(db.String(50))

    basket = db.relationship("Basket")
    yarn = db.relationship("Yarn")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<BasketYarn b_y_id=%s yarn_id=%s>" % (self.basket_yarn_id,
                                                      self.yarn_id)


class BasketYarnPhoto(db.Model):
    """Photo stored with BasketYarn"""

    __tablename__ = "basket_yarn_photos"

    photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    basket_yarn_id = db.Column(db.Integer,
                               db.ForeignKey("basket_yarns.basket_yarn_id"),
                               nullable=False)
    photo = db.Column(db.String(400), nullable=False, unique=True)

    basket_yarn = db.relationship("BasketYarn")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<BasketYarnPhoto photo_id=%s basket_yarn_id=%s>" % (self.photo_id,
                                                                    self.basket_yarn_id)


##############################################################################
# Helper functions

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
