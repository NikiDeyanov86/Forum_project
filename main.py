from flask import Flask
from flask import render_template, request, redirect, make_response, url_for

from flask_login import login_user, login_required, current_user, logout_user

from database import db_session, init_db
from models import User, Topic, Post


app = Flask(__name__)

init_db()

@app.teardown_appcontext
def shutdown_context(exception=None):
    db_session.remove()

@app.route('/', methods=['GET'])
def homepage():
    return render_template("home.html")
