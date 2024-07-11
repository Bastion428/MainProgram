from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')
        error = False

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already is use', category='error')
            error = True
        if pass1 != pass2:
            flash('Passwords do not match', category='error')
            error = True
        if len(pass1) < 6:
            flash('Password must be 6 characters or more', category='error')
            error = True
        if len(username) < 6:
            flash('Username must be 6 characters or more', category='error')
            error = True
        if not error:
            new_user = User(username=username,  # type: ignore[call-arg]
                            password=generate_password_hash(pass1, method='pbkdf2:sha256'))  # type: ignore[call-arg]
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Succesfully created account!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/login', methods=["GET", "POST"])
def login():
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

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
