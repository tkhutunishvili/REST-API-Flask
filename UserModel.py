from flask_sqlalchemy import SQLAlchemy
from settings import app
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	public_id = db.Column(db.String(50), unique = True)
	username = db.Column(db.String(100))
	password = db.Column(db.String(80))

	def username_password_match(_username, _password):
		user = User.query.filter_by(username=_username).filter_by(password=_password).first()
		if user is None:
			return False
		else:
			return True

	def getAllUsers():
		return User.query.all()

	def createUser(_username, _password):
		new_user = User(public_id = str(uuid.uuid4()), username=_username, password=generate_password_hash(_password))
		db.session.add(new_user)
		db.session.commit()
	def deleteUser(_username):
		is_successful = User.query.filter_by(username=_username).delete()
		db.session.commit()
		return bool(is_successful)
