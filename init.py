from server_pkg.app import create_app,db
from flask_migrate import upgrade,migrate,init,stamp
from server_pkg.models import  Tour, User, Location
from server_pkg.app import bcrypt

# from SQL import SQL
import os

def deploy():
	"""Run deployment tasks."""
	app = create_app()
	app.app_context().push()
	db.create_all()

	# migrate database to latest revision
	init()
	stamp()
	migrate()
	upgrade()
	
# deploy()