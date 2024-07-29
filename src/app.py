"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))

    response_body = {
        "results": users,
    }

    return jsonify(response_body), 200

@app.route('/user/favorites', methods=['GET'])
def get_users_favorites():

    user = User.query.get(1)

    def planets(f):
        if f.planet != None : return True

    def vehicules(f):
        if f.vehicule != None : return True
        
    def characters(f):
        if f.character != None : return True

    planets = list(map(lambda x: x.serialize(),list(filter(planets, user.favorites))))
    vehicules = list(map(lambda x: x.serialize(),list(filter(vehicules, user.favorites))))
    characters = list(map(lambda x: x.serialize(),list(filter(characters, user.favorites))))

    response_body = {
        "planets": planets,
        "vehicules": vehicules,
        "characters": characters
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():

    characters = Character.query.all()
    characters = list(map(lambda x: x.serialize(), characters))

    response_body = {
        "results": characters,
    }

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):

    characters = Character.query.get(people_id)
    characters = characters.serialize()


    response_body = {
        "results": characters,
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    planets = list(map(lambda x: x.serialize(), planets))

    response_body = {
        "results": planets,
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets_by_id(planet_id):

    planet = Planet.query.get(planet_id)
    planet = planet.serialize()

    response_body = {
        "results": planet,
    }

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=["POST"])
def add_favorite_planet(planet_id):

    favorite = Favorite()
    favorite.user_id = 1
    favorite.planet_id = planet_id

    db.session.add(favorite)
    db.session.commit()

    favorite = Favorite.query.get(favorite.id)
    favorite = favorite.serialize()

    response_body = {
        "results": favorite,
    }

    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def add_favorite_people(people_id):

    favorite = Favorite()
    favorite.user_id = 1
    favorite.people_id = people_id

    db.session.add(favorite)
    db.session.commit()

    favorite = Favorite.query.get(favorite.id)
    favorite = favorite.serialize()

    response_body = {
        "results": favorite,
    }

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=["DELETE"])
def delete_favorite_planet(planet_id):

    favorite = Favorite.query.filter_by(user_id=1).filter_by(planet_id=planet_id).first()

    db.session.delete(favorite)
    db.session.commit()

    response_body = {
        "message": "Favorite was successfully deleted",
    }

    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=["DELETE"])
def delete_favorite_people(people_id):

    favorite = Favorite.query.filter_by(user_id=1).filter_by(character_id=people_id).first()

    db.session.delete(favorite)
    db.session.commit()

    response_body = {
        "message": "Favorite was successfully deleted",
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
