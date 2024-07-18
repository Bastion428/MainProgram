from flask import Blueprint, render_template, session
from flask_login import login_required

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def collection():
    return render_template('collection.html')

@views.route('/add-game')
@login_required
def add_game():
    return render_template('add_game.html')

