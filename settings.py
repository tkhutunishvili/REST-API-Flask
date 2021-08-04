from flask import Flask

app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/animal_db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
