from dataclasses import dataclass
from importlib.resources import path
import json
import time
from flask import render_template, redirect, flash, url_for, session, request, send_from_directory
from datetime import timedelta
import flask_login
from sqlalchemy.exc import IntegrityError, DataError, DatabaseError, InterfaceError, InvalidRequestError
from werkzeug.routing import BuildError
from werkzeug.utils import secure_filename
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, login_required
from server_pkg.app import create_app, db, login_manager, bcrypt
# , images
from server_pkg.models import Tour, User, Location
from server_pkg.forms import *
import os
import imghdr
from SQL import SQL

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from dynaconf import FlaskDynaconf
# from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()
FlaskDynaconf(app)
# socketio = SocketIO(app, engineio_logger=True, ping_timeout=5, ping_interval=5)
GoogleMaps(
    app,
    # key="AIzaSyB2bXKNDezDf6YNVc-SauobynNHPo4RJb8"
)


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)

# home page


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    if request.method == "POST":
        print(request.form["search_box_text"])
        tours = Tour.query.filter(Tour.name.like(
            "%" + request.form["search_box_text"] + "%")).all()
        search_text = request.form["search_box_text"]
    else:
        search_text = ""
        tours = Tour.query.all()
    print(tours)
    mkr = []
    for i in tours:
        mkr.append({
            "icon": "//maps.google.com/mapfiles/ms/icons/yellow-dot.png",
            "lat": i.latitude,
            "lng": i.longitude,
            "infobox": (
                    """<h2>{0}</h2><br>
                    <h3>{1}</h3>
                    <a href="explore_tour/{2}"><h5>open details</h5></a>
                    <img src="static/{3}.png" style="width: 50px; height: 50px; margin-left: 10px;">""".format(i.name, i.description, i.id, i.photos)
            ),
        })
    print(mkr)

    trdmap = Map(
        identifier="trdmap",
        varname="trdmap",
        style=(
            "height:100%;"
            "width:100%;"
            # "top:0;"
            # "left:0;"
            # "position:absolute;"
            # "z-index:200;"
        ),
        lat=20.593684,
        lng=78.96288,
        markers=mkr,
        zoom=12,
        cluster=True,
    )

    return render_template("index.html", trdmap=trdmap,
                           GOOGLEMAPS_KEY=request.args.get("apikey"),search_text=search_text)

# user authentication


@app.route("/login", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("login.html",
                           form=form,
                           text="Login",
                           title="Login",
                           btn_action="Login"
                           )


@app.route("/register", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("register.html",
                           form=form,
                           text="Create account",
                           title="Register",
                           btn_action="Register account"
                           )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/profile")
@login_required
def profile():
    user = User.query.filter_by(id=flask_login.current_user.id).first()
    print(user)
    return render_template("profile.html", user=user, text="Profile of " + user.username)


@app.route("/profile_reward")
@login_required
def profile_share():
    user = User.query.filter_by(id=flask_login.current_user.id).first()
    print(user)
    return render_template("profile.html", user=user, text="Share on your social media")


@app.route("/add_tour", methods=("GET", "POST"))
@login_required
def addTour():
    form = Tour_form()

    if form.validate_on_submit():
        try:
            name = form.name.data
            longitude = form.longitude.data
            latitude = form.latitude.data
            # photos = form.photos.data
            # file_name = images.save(photos)
            # print(file_name)
            site = form.site.data
            landmarks = form.landmarks.data
            opening_timing = form.opening_timing.data
            description = form.description.data

            newtour = Tour(
                name=name,
                longitude=longitude,
                latitude=latitude,
                site=site,
                landmarks=landmarks,
                opening_timing=opening_timing,
                description=description,
                uid=flask_login.current_user.id,
            )
            user = User.query.filter_by(id=flask_login.current_user.id).first()
            db.session.add(newtour)
            user.coins = user.coins + 10
            db.session.commit()
            flash(f"tour Succesfully created", "success")

            # return redirect(url_for('index'))
        #     user = User.query.filter_by(email=form.email.data).first()
        except Exception as e:
            print(e)
            flash(e, "danger")

    return render_template("addTour.html",
                           form=form,
                           text="Add Tour",
                           title="Add Tour"
                           )


@app.route("/add_location", methods=("GET", "POST"))
@login_required
def addLocation():
    form = Location_form()

    if form.validate_on_submit():
        try:
            name = form.name.data
            _type = form.type.data
            site = form.site.data
            longitude = form.longitude.data
            latitude = form.latitude.data
            opening_timing = form.opening_timing.data
            photos = form.photos.data
            description = form.description.data
            other_type = form.other_type.data
            decoded = request.form
            print("POST", decoded)
            TourID = int(decoded["TourID"])  # default -1
            print(TourID)

            newlocation = Location(
                name=name,
                type=_type,
                site=site,
                longitude=longitude,
                latitude=latitude,
                opening_timing=opening_timing,
                description=description,
                other_type=other_type,
                tid=TourID,
            )
            user = User.query.filter_by(id=flask_login.current_user.id).first()
            db.session.add(newlocation)
            user.coins = user.coins + 2
            db.session.commit()
            flash(f"newlocation Succesfully created", "success")

            return redirect(url_for('index'))
        #     user = User.query.filter_by(email=form.email.data).first()
        #     if check_password_hash(user.pwd, form.pwd.data):
        #         login_user(user)
        #         return redirect(url_for('index'))
        #     else:
        #         flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")
    tours = Tour.query.filter_by(uid=flask_login.current_user.id).all()
    print(tours[0].name)
    return render_template("addLocation.html",
                           form=form,
                           text="Add Location",
                           title="Add Location",
                           tours=tours
                           )


@app.route("/added_tour")
@login_required
def addedTour():
    tours = Tour.query.filter_by(uid=flask_login.current_user.id).all()
    locations = []
    for tour in tours:
        locations.append(Location.query.filter_by(tid=tour.id).all())
    print(tours)
    print(locations)
    return render_template("addedTour.html", tours=tours, locations=locations)


@app.route("/explore_tour/<int:tourId>")
def exploreTour(tourId):
    locations = Location.query.filter_by(tid=tourId).all()
    print(locations)
    mkr = []
    for i in locations:
        mkr.append({
            "icon": "//maps.google.com/mapfiles/ms/icons/yellow-dot.png",
            "lat": i.latitude,
            "lng": i.longitude,
            "infobox": (
                    """<h2>{0}</h2><br>
                    <h3>{1}</h3>
                    <a href="http://127.0.0.1:5000/explore_location/{2}"><h5>open details</h5></a>
                    <img src="static/{3}.png" style="width: 50px; height: 50px; margin-left: 10px;">""".format(i.name, i.description, i.id, i.photos)
            ),
        })
    print(mkr)

    trdmap = Map(
        identifier="trdmap",
        varname="trdmap",
        style=(
            "height:1000px;"
            "width:1000px;"
        ),
        lat=20.593684,
        lng=78.96288,
        markers=mkr,
        zoom=12,
        cluster=True,
    )
    tour = Tour.query.filter_by(id=tourId).first()
    print(tour)
    return render_template("exploreTour.html", tour=tour, trdmap=trdmap,
                           GOOGLEMAPS_KEY=request.args.get("apikey"))


@app.route("/explore_location/<int:locationId>")
def exploreLocation(locationId):
    loc = Location.query.filter_by(id=locationId).first()
    print(loc)
    return render_template("exploreLocation.html", loc=loc)


if __name__ == "__main__":
    app.run(debug=True)
    # socketio.run(app, debug=True)
