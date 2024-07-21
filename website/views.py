from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, current_user
from .models import MyGame
from . import db

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def collection():
    return render_template('collection.html')


@views.route('/my-game/<title>', methods=["GET", "POST"])
@login_required
def my_game(title):
    if request.method == "GET":
        flash('Please choose a game directly from your collection.', category='error')
        return redirect(url_for('views.collection'))

    game_id = request.form.get('id')
    game = MyGame.query.get(game_id)

    if current_user.id != game.user_id:
        flash('You are not authorized to view this game page.', category='error')
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


@views.route('/delete-game', methods=["DELETE"])
@login_required
def delete_game():
    game = request.get_json()
    game_id = game['game_id']
    game = MyGame.query.get(game_id)

    if game:
        if game.user_id == current_user.id:
            db.session.delete(game)
            db.session.commit()
            flash("Game successfully deleted", category='success')
            return make_response("Success", 204)
        else:
            flash("Not authorized to delete this game!", category='error')
    else:
        flash("Game not in your collection and unable to be deleted", category='error')

    return make_response("Error", 400)

    
