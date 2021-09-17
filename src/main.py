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
from models import db, User, Planet, Character, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
def get_all_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users)) 
    print(all_users)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "Users": all_users
    }
    return jsonify(response_body), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    user = User.query.get(id)
    print(user)
    return jsonify(user.serialize()), 200 

@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.get_json()
    if email is None or password is None:
        return jsonify({"msg": "Invalid username or password"}), 401
    user = User(username=request_body["username"], email=request_body["email"], password=request_body["password"])
    db.session.add(user)
    db.session.commit()
    print("User created: ", request_body)
    return jsonify(request_body), 200
 

@app.route('/planet', methods=['GET'])
def get_all_planet():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets)) 
    print(all_planets)
    response_body = {
        "msg": "Hello, this is your GET /planet response ",
        "Planets": all_planets
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planet(id):
    planet = Planet.query.get(id)
    print(planet)
    return jsonify(planet.serialize()), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    request_body = request.get_json()
    if name is None or population is None or terrain is None or climate is None or orbital_period is None or rotation_period is None or diameter is None or type is None:
        return jsonify({"msg": "Bad name or population or terrain or climate or orbital_period or rotation_period or diameter or type"}), 401
    planet = Planet(name=request_body["name"], population=request_body["population"], terrain=request_body["terrain"], climate=request_body["climate"], orbital_period=request_body["orbital_period"], rotation_period=request_body["rotation_period"], diameter=request_body["diameter"], type=request_body["type"])
    db.session.add(planet)
    db.session.commit()
    print("Planet created: ", request_body)
    return jsonify(request_body), 200

@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
    request_body = request.get_json()
    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"msg": "character not found"}), 404
    if "name" in request_body:
        planet.name = request_body["name"]
    if "population" in request_body:
        planet.population = request_body["population"]
    if "terrain" in request_body:
        planet.terrain = request_body["terrain"]
    if "climate" in request_body:
        planet.climate = request_body["climate"]
    if "orbital_period" in request_body:
        planet.orbital_period = request_body["orbital_period"]    
    if "rotation_period" in request_body:
        planet.rotation_period = request_body["rotation_period"]
    if "diameter" in request_body:
        planet.diameter = request_body["diameter"]
        
    db.session.commit()

    print("Planet updated: ", request_body)
    return jsonify(request_body), 200

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"msg": "character not found"}), 404

    db.session.delete(planet)
    db.session.commit()
    response_body = {
         "msg": "Planet deleted successfully",
    }
    return jsonify(response_body), 200


@app.route('/character', methods=['GET'])
def get_all_character():
    all_characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters))
    print(all_characters)
    response_body = {
        "msg": "Hello, this is your GET /character response ",
        "Characters": all_characters
    } 
    return jsonify(response_body), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_single_character(id):
    character = Character.query.get(id)
    print(character)
    return jsonify(character.serialize()), 200

@app.route('/character', methods=['POST'])
def create_character():
    request_body = request.get_json()
    if name is None or gender is None or hair_color is None or eye_color is None or birth_year is None or height is None or skin_color is None or type is None:
        return jsonify({"msg": "Bad name or gender or hair_color or eye_color or birth_year or height or skin_color or type"}), 401
    character = Character(name=request_body["name"], gender=request_body["gender"], hair_color=request_body["hair_color"], eye_color=request_body["eye_color"], birth_year=request_body["birth_year"], height=request_body["height"], skin_color=request_body["skin_color"], type=request_body["type"])
    db.session.add(character)
    db.session.commit()
    print("Character created: ", request_body)
    return jsonify(request_body), 200

@app.route('/character/<int:id>', methods=['PUT'])
def update_character(id):
    request_body = request.get_json()
    character = Character.query.get(id)

    if character is None:
        return jsonify({"msg": "character not found"}), 404
    if "name" in request_body:
        character.name = request_body["name"]
    if "gender" in request_body:
        character.gender = request_body["gender"]
    if "hair_color" in request_body:
        character.hair_color = request_body["hair_color"]
    if "eye_color" in request_body:
        character.eye_color = request_body["eye_color"]
    if "birth_year" in request_body:
        character.birth_year = request_body["birth_year"]    
    if "height" in request_body:
        character.height = request_body["height"]
    if "skin_color" in request_body:
        character.skin_color = request_body["skin_color"]
    
    db.session.commit()

    print("Character updated: ", request_body)
    return jsonify(request_body), 200

@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get(id)

    if character is None:
        return jsonify({"msg": "Invalid character"}), 401

    db.session.delete(character)
    db.session.commit()
    response_body = {
         "msg": "Character deleted successfully",
    }
    return jsonify(response_body), 200


@app.route("/favorites", methods=["GET"])
def get_favorites():
    all_favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(),all_favorites))
    print(all_favorites)
    response_body = {
        "msg": "Hello, this is your GET /favorites response ",
        "Favorites": all_favorites
        } 
    return jsonify(response_body), 200

@app.route('/favorite', methods=['POST'])
def add_favorite():
    request_body = request.get_json()
    if request_body is None:
        return "The request body is null", 400
    favorite = Favorite(favorite_id=request_body["favorite_id"], type=request_body["type"], user_id=request_body["user_id"])
    db.session.add(favorite)
    db.session.commit()
    print("Favorite added: ", request_body)
    return jsonify(request_body), 200

@app.route('/favorite/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    favorite = Favorite.query.get(id)
    if favorite is None:
        return jsonify({"msg": "Invalid favorite"}), 401
    db.session.delete(favorite)
    db.session.commit()
    response_body = {
         "msg": "Favorite deleted successfully",
    }
    return jsonify(response_body), 200







  



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
