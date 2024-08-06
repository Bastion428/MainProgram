from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import MyGame
from . import db
from werkzeug.datastructures import ImmutableMultiDict
from sqlalchemy.dialects import postgresql
import requests

NO_IMAGE = "https://rpvalleyradiologists.com/wp-content/uploads/2021/06/no-image-available-sm.jpg"

views = Blueprint('views', __name__)


def game_dictionary(form: ImmutableMultiDict):
    game_dict = {}
    for key in form:
        game_dict[key] = form.get(key)

    game_dict['own'] = True if game_dict['own'] == 'Yes' else False
    game_dict['beat'] = True if game_dict['beat'] == 'Yes' else False

    return game_dict


def new_game(game_info: dict):
    if not game_info['image']:
        image = NO_IMAGE
    else:
        image = game_info['image']

    new_game = MyGame(title=game_info['title'], 
                    year=game_info['year'],
                    platform=game_info['platform'], 
                    developer=game_info['developer'],
                    image = image,
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

@views.route('/help')
@login_required
def help():
    return render_template('help.html')


@views.route('/my-game/<title>', methods=["POST"])
@login_required
def my_game(title):
    game_id = request.form.get('id')   
    game = MyGame.query.get(game_id)

    if not game:
        flash('Not an existing game.', category='error')
        return redirect(url_for('views.collection'))
        
    if current_user.id != game.user_id:
        flash('Not authorized to view this game page.', category='error')
        return redirect(url_for('views.collection'))

    return render_template('my_game.html', game=game)


@views.route('/add-game', methods=["GET", "POST"])
@login_required
def add_game():
    if request.method == 'POST':
        game_info = game_dictionary(request.form)

        game = MyGame.query.filter_by(title=game_info['title'],
                                      year=game_info['year'],
                                      platform=game_info['platform'],
                                      user_id=current_user.id
                                      ).first()

        if game:
            flash('Game already in your collection', category='error')
        else:
            return new_game(game_info)

    return render_template('add_game.html')


@views.route('/edit-game/<title>', methods=["POST"])
@login_required
def view_edit(title):
    game_id = request.form.get('id')   
    game = MyGame.query.get(game_id)

    if game.image == NO_IMAGE:
        game.image = ""

    if game.user_id != current_user.id:
        flash("Not authorized to edit this game!", category='error')
        return redirect(url_for('views.collection'))

    if not game:
        flash("Game not in your collection and unable to be edited", category='error')
        return redirect(url_for('views.collection'))   

    return render_template('edit_game.html', game=game)
    


@views.route('/update-game', methods=["PUT"])
@login_required
def edit_game():
    game_dict = request.get_json()
    game_id = game_dict['id']

    game_dict['own'] = True if game_dict['own'] == 'Yes' else False
    game_dict['beat'] = True if game_dict['beat'] == 'Yes' else False

    if 'image' not in game_dict or game_dict['image'] == "":
        game_dict['image'] = NO_IMAGE

    game = MyGame.query.get(game_id)

    game_exists = MyGame.query.filter(MyGame.id != game_id, 
                                MyGame.title==game_dict['title'],
                                MyGame.year==game_dict['year'],
                                MyGame.platform==game_dict['platform'],
                                MyGame.user_id==current_user.id
                                ).first()

    if not game:
        return "Game not in your collection and unable to be edited", 401
    
    if game_exists:
        return "Game already exists in your collection! Edit title, release year, or platform.", 400

    if game.user_id != current_user.id:
        return "Not authorized to edit this game!", 401
    
    del game_dict['id']
    MyGame.query.filter(MyGame.id == game_id).update(game_dict)
    db.session.commit()

    flash("Game successfully updated!", category='success')
    return {}, 200


@views.route('/search')
@login_required
def search_game():
    query = request.args.get('query')
    results = MyGame.query.filter(MyGame.title.contains(query), MyGame.user_id == current_user.id)

    #print(results.statement.compile(compile_kwargs={"literal_binds": True}))

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
        return {}, 400  

    if game.user_id == current_user.id:
        db.session.delete(game)
        db.session.commit()

        if req_loc != '/':
            flash("Game successfully deleted", category='success')
        return {}, 204
    else:
        flash("Not authorized to delete this game!", category='error')
        
    return {}, 400


@views.route('/steam-game')
@login_required
def steam_game():
    req = request.get_json()
    res = requests.post("http://localhost:6523/steam-search", json=req)

    return res.json()

    