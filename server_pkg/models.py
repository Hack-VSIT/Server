from email.policy import default
from server_pkg.app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    # user account variables, can't be edited by the user
    status = db.Column(db.Integer, nullable=False, default=0)
    tour = db.Column(db.Integer, nullable=False, default=0)
    cred = db.Column(db.Integer, nullable=False, default=3)
    # FK reference
    tours = db.relationship('Tour', backref='user_det', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Tour(db.Model):
    __tablename__ = "tour"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    photos = db.Column(db.String(300), unique=True)
    site = db.Column(db.String(100))
    landmarks = db.Column(db.String(100))
    opening_timing = db.Column(db.String(100))
    description = db.Column(db.String(300), nullable=False)
    # Tour variables, can't be edited by the user
    rating = db.Column(db.Integer, nullable=False, default=3)
    hits = db.Column(db.Integer, nullable=False, default=0)
    reviews = db.Column(db.String(300))
    # FK reference
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tours = db.relationship('Location', backref='tour_det', lazy=True)

    def __repr__(self):
        return '<Tour %r>' % self.name


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Integer, nullable=False, default=0)
    site = db.Column(db.String(100), nullable=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    opening_timing = db.Column(db.String(100), nullable=True)
    photos = db.Column(db.String(300), nullable=True, unique=True)
    description = db.Column(db.String(300), nullable=False)
    other_type = db.Column(db.String(100), nullable=True)
    # Tour variables, can't be edited by the user
    hits = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, nullable=False, default=3)
    reviews = db.Column(db.String(300))
    # FK reference
    tid = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)

    def __repr__(self):
        return '<Location %r>' % self.name
