from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import requests, json

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.collection'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')
        error = False

        user = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user:
            flash('Username already in use', category='error')
            error = True
        if user_email:
            flash('Email already in use', category='error')
            error = True

        info = { 'name': name, 'email': email, 'username': username, 'pass1': pass1, 'pass2': pass2}
        res = requests.post("http://localhost:4688/validate-user", data=info)

        message_list = res.json()['messages']

        for message in message_list:
            flash(message, category='error')
     
        if not error and res.status_code == 200:
            password = generate_password_hash(pass1, method='pbkdf2:sha256')
            new_user = User(name=name,email=email,username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            info = { 'name': name, 'email': email, 'username': username, 'password': pass1}
            requests.post("http://localhost:7134/send-signup", data=info)

            flash('Succesfully created account!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html")


@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.collection'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Successfully logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.collection'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist', category='error')

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
