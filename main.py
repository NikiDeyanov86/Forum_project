import uuid
import os

from flask import Flask
from flask import render_template, request, redirect, make_response, url_for

from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from database import db_session, init_db
from login import login_manager
from models import User, Topic, Post


app = Flask(__name__)

login_manager.init_app(app)
init_db()


@app.teardown_appcontext
def shutdown_context(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def homepage():
    topics = Topic.query.all()
    print(current_user)
    print(current_user.__dict__)

    return render_template("home.html", topics=topics, user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password)
        db_session.add(user)
        db_session.commit()

        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@ app.route('/logout')
@ login_required
def logout():
    current_user.login_id = None
    db_session.commit()
    logout_user()

    return redirect(url_for('homepage'))


@ app.route('/add_topic', methods=['GET', 'POST'])
@ login_required
def add_topic():
    if request.method == 'GET':
        return render_template("add_topic.html")
    else:
        title = request.form['title']
        description = request.form['description']

        topic = Topic(title=title, description=description)
        db_session.add(topic)
        db_session.commit()

        return redirect(url_for('homepage'))
