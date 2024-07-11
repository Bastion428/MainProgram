from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')

        if pass1 != pass2:
            flash('Passwords do not match', category='error')
        elif len(pass1) < 6:
            flash('Password must be 6 characters or more', category='error')
        elif len(username) < 6:
            flash('Username must be 6 characters or more', category='error')
        else:
            flash('Succesfully created account!', category='success')

    return render_template("sign_up.html")


@auth.route('/', methods=["GET", "POST"])
def login():
    info = request.form
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return redirect(url_for("auth.login"))
