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
app.secret_key = "ssucuuh398nuwetubr33rcuhne"
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
    if 'login_id' in current_user.__dict__:
        return redirect(url_for('homepage'))

    if request.method == 'GET':
        return render_template("register.html", user=current_user)
    else:
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password)
        db_session.add(user)
        db_session.commit()

        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'login_id' in current_user.__dict__:
        return redirect(url_for('homepage'))

    response = None
    if request.method == 'GET':
        response = make_response(render_template('login.html',
                                                 user=current_user))
    else:
        response = make_response(redirect(url_for('homepage')))

        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password,
                                        request.form['password']):
            user.login_id = str(uuid.uuid4())
            db_session.commit()
            login_user(user)
    return response


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
        return render_template("add_topic.html", user=current_user)
    else:
        title = request.form['title']
        description = request.form['description']

        topic = Topic(title=title, description=description)
        db_session.add(topic)
        db_session.commit()

        return redirect(url_for('homepage'))
