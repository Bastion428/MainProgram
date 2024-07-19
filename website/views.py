from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import MyGame
from . import db

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def collection():
    return render_template('collection.html')


@views.route('/my-game', methods=["GET", "POST"])
@login_required
def my_game():
    if request.method == "GET":
        flash('No game has been specified. Please choose one from your collection.', category='error')
        return redirect(url_for('views.collection'))

    game_id = request.form.get('id')
    game = MyGame.query.get(game_id)

    if current_user.id != game.user_id:
        flash('You are not authorized to view this game.', category='error')
        return redirect(url_for('views.collection'))

    return render_template('my_game.html', game=game)

@views.route('/add-game', methods=["GET", "POST"])
@login_required
def add_game():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        platform = request.form.get('platform')
        developer = request.form.get('developer')
        publisher = request.form.get('publisher')
        hours = request.form.get('hours')
        score = request.form.get('score')
        own = request.form.get('own')
        beat = request.form.get('beat')
        review = request.form.get('review')
        error = False

        game = MyGame.query.filter_by(title=title,
                                      year=year,
                                      platform=platform,
                                      user_id=current_user.id
                                      ).first()

        own = True if own else False
        beat = True if beat else False

        if game:
            flash('Game already in your collection', category='error')
            error = True
        if not error:
            new_game = MyGame(title=title, year=year,
                              platform=platform, developer=developer,
                              publisher=publisher, play_hours=hours,
                              score=score, own=own, beat=beat,
                              review=review, user_id=current_user.id
                              )
            db.session.add(new_game)
            db.session.commit()
            flash('Game added to your collection!', category='success')
            return redirect(url_for("views.collection"))

    return render_template('add_game.html')
