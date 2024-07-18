from flask import Blueprint, render_template, session
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def collection():
    return render_template('collection.html', user=current_user)
