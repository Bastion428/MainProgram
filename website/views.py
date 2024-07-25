from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, jsonify
from flask_login import login_required, current_user
from .models import MyGame
from . import db

views = Blueprint('views', __name__)

def new_game(game_info: dict):
    new_game = MyGame(title=game_info['title'], 
                    year=game_info['year'],
                    platform=game_info['platform'], 
                    developer=game_info['developer'],
                    publisher=game_info['publisher'], 
                    play_hours=game_info['hours'],
                    score=game_info['score'], 
                    own=game_info['own'], 
                    beat=game_info['beat'],
                    review=game_info['review'], 
                    user_id=current_user.id
                    )
    db.session.add(new_game)
    db.session.commit()
    flash('Game added to your collection!', category='success')
    return redirect(url_for("views.collection"))


@views.route('/')
@login_required
def collection():
    return render_template('collection.html')


@views.route('/my-game/<title>', methods=["POST"])
@login_required
def my_game(title):
    game_id = request.form.get('id')
    if not game_id:
        game_id = request.form.get('auto_id')
        
    game = MyGame.query.get(game_id)

    if not game:
        flash('Not an existing game.', category='error')
        return redirect(url_for('views.collection'))
        
    if current_user.id != game.user_id:
        flash('You are not authorized to view this game page.', category='error')
        return redirect(url_for('views.collection'))

    return render_template('my_game.html', game=game)

@views.route('/add-game', methods=["GET", "POST"])
@login_required
def add_game():
    if request.method == 'POST':
        game_info = {}
        game_info['title'] = request.form.get('title')
        game_info['year'] = request.form.get('year')
        game_info['platform'] = request.form.get('platform')
        game_info['developer'] = request.form.get('developer')
        game_info['publisher'] = request.form.get('publisher')
        game_info['hours'] = request.form.get('hours')
        game_info['score'] = request.form.get('score')
        game_info['own'] = request.form.get('own')
        game_info['beat'] = request.form.get('beat')
        game_info['review'] = request.form.get('review')

        game = MyGame.query.filter_by(title=game_info['title'],
                                      year=game_info['year'],
                                      platform=game_info['platform'],
                                      user_id=current_user.id
                                      ).first()

        game_info['own'] = True if game_info['own'] else False
        game_info['beat'] = True if game_info['beat'] else False

        if game:
            flash('Game already in your collection', category='error')
        else:
            return new_game(game_info)

    return render_template('add_game.html')


@views.route('/search')
@login_required
def search_game():
    query = request.args.get('query')
    results = MyGame.query.filter(MyGame.title.contains(query), MyGame.user_id == current_user.id)

    suggestions = []
    for game in results:
        suggestions.append({ 'value': game.title, 'data': game.id })

    return jsonify({"suggestions":suggestions})


@views.route('/delete-game', methods=["DELETE"])
@login_required
def delete_game():
    game = request.get_json()
    game_id = game['game_id']
    req_loc = game['req_loc']
    game = MyGame.query.get(game_id)

    if not game:
        flash("Game not in your collection and unable to be deleted", category='error')
        return make_response("Error", 400)    

    if game.user_id == current_user.id:
        db.session.delete(game)
        db.session.commit()

        if req_loc != '/':
            flash("Game successfully deleted", category='success')

        return make_response("Success", 204)
    else:
        flash("Not authorized to delete this game!", category='error')
        

    return make_response("Error", 400)
