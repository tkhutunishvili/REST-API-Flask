from flask import Flask, jsonify, request, Response, make_response

import uuid
import json
from UserModel import User
from AnimalModel import *
from settings import *

import jwt, datetime
from functools import wraps

from  werkzeug.security import generate_password_hash, check_password_hash

# import logging
from logging.config import fileConfig

fileConfig('logging.cfg')


app.config['SECRET_KEY'] = 'animals'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
   
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
   
    return decorated
@app.route('/', methods =['GET'])
def empty_page():
    return make_response('Main Page', 200)

@app.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    request_data = request.get_json()
    app.logger.debug('POST %s', request.get_json())
    if not request_data or not request_data['username'] or not request_data['password']:
        # returns 401 if any username or / and password is missing
        return make_response(
            'Could not verify Login',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
   
    user = User.query\
        .filter_by(username = request_data['username'])\
        .first()
   
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify user',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
   
    if check_password_hash(user.password, request_data['password']):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
   
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify Password',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )
   
@app.route('/user', methods =['GET'])
@token_required
def get_all_users():
    # querying the database
    # for all the entries in it
    users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json 
        # to the response list
        output.append({
            'public_id': user.public_id,
            'username' : user.username,
            'password' : user.password
        })
   
    return jsonify({'users': output})

@app.route('/register', methods=['POST'])
# @token_required
def create_user():
    # create new user
    request_data = request.get_json()
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
    app.logger.debug('POST %s', request.get_json())
    app.logger.debug('Add new user %s, %s', request_data['username'], request_data['password'])
    hashed_password = generate_password_hash(request_data['password'], method='sha256')
    if not User.query.filter_by(username=request_data['username']).first():
        new_user = User(public_id=str(uuid.uuid4()), username=request_data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # return jsonify({'message':'New user created!'})
        return jsonify({'message':'New user created!'})
    return jsonify({'message':'User already exists'})

def ValidAnimalObject(animalObject):
    if ('name' in animalObject and 'price' in animalObject and 'centerid' in animalObject and 'species' in animalObject and 'age' in animalObject):
        return True
    else:
        return True

def valid_put_request_data(animalObject):
    if ('name' in animalObject and 'price' in animalObject and 'centerid' in animalObject and 'species' in animalObject and 'age' in animalObject):
        return True
    else:
        return False


@app.route("/animals")
@token_required
def get_animals(current_user):
    """Return full list of animals."""
    app.logger.debug("Debug Logging")

    return jsonify({'animals': Animals.get_all_animals()})

@app.route("/animals/<int:centerid>")
@token_required
def get_animal(current_user, centerid):
    """Return detailed information about animal."""
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
    return jsonify({'animal': Animals.get_animal(centerid)})

    # return_value = Animals.get_animal(centerid)
    # return jsonify(return_value)

@app.route("/centers")
@token_required
def get_centers(current_user):
    """Return full list of animals."""

    return jsonify(Animals.get_centers())

@app.route("/centers/<int:centerid>")
@token_required
def get_centers_id(current_user, centerid):
    """Return detailed information about animal."""
    return jsonify({'center': Animals.get_centers_id(centerid)})

    # return_value = Animals.get_centers_id(centerid)
    # return jsonify(return_value)

@app.route("/species")
@token_required
def get_species(current_user):
    """Return Animals ID and Name for 1 species."""
    return jsonify(Animals.get_species())

    # return_value = Animals.get_species_id(species)
    # return jsonify(return_value)

@app.route("/species/<species>")
@token_required
def get_species_id(current_user, species):
    """Return Animals ID and Name for 1 species."""
    return jsonify({'species': Animals.get_species_id(species)})

    # return_value = Animals.get_species_id(species)
    # return jsonify(return_value)

@app.route("/animals", methods=['POST'])
@token_required
def add_animal(current_user):
    """add detailed information about new animal."""
    app.logger.debug('POST %s', request.get_json())

    request_data = request.get_json()
    app.logger.debug('Add animal: %s, %s, %s, %s, %s, %s', request_data['centerid'], request_data['name'], request_data['description'], request_data['age'], request_data['species'], request_data['price'])
    if(ValidAnimalObject(request_data)):
        Animals.add_animal(
            request_data['centerid'], 
            request_data['name'], 
            request_data['description'], 
            request_data['age'], 
            request_data['species'], 
            request_data['price']
        )
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/animals" + str(request_data['centerid'])
        return jsonify({'message':'New Animal was added!'})
    else:
        invalidAnimalObjectErrorMsg = {
            "error": "Invalid Animal object passed in request",
            "helpString": "Data passed in similar to this {'centerid': 123456789, aname': 'animalname', 'description': 'animaldescription', 'age': 5, 'species': 'animaltype', 'price': 12.45}"
        }
        response = Response(json.dumps(invalidAnimalObjectErrorMsg), status=400, mimetype='application/json')
        return response;

@app.route('/animals/<int:centerid>', methods=['PUT'])
@token_required
def replace_animal(current_user, centerid):
    app.logger.debug('PUT %s', request.get_json())
    request_data =  request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidAnimalObjectErrorMsg = {
            "error": "Invalid animal object passed in request",
            "helpString": "Data passed in similar to this {'centerid': 123456789, 'name': 'animalname', 'description': 'animaldescription', 'age': 5, 'species': 'animaltype', 'price': 12.45}"
        }
        response = Response(json.dumps(invalidAnimalObjectErrorMsg), status=400, mimetype='application/json')
        return response

        Animals.replace_animals(
            request_data['centerid'],
            request_data['name'], 
            request_data['description'], 
            request_data['age'], 
            request_data['species'], 
            request_data['price']
        )
    app.logger.debug('Update animal: %s, %s, %s, %s, %s, %s', request_data['centerid'], request_data['name'], request_data['description'], request_data['age'], request_data['species'], request_data['price'])
    response = Response("", status=204)
    return jsonify({'message':'Animal data was updated!'})

@app.route("/animals/<int:centerid>", methods=['DELETE'])
@token_required
def delete_animal(current_user, centerid):
    app.logger.debug('DELETE %s', request.get_json())
    if(Animals.delete_animal(centerid)):
        response = Response("", status=204)
        return jsonify({'message':'Animal was deleted!'})
    invalidAnimalObjectErrorMsg = {
        "error": "Animal with provided ID number not found, no animal was deleted.",
    }
    response = Response(json.dumps(invalidAnimalObjectErrorMsg), status=404, mimetype='application/json')
    return response    


if __name__ == "__main__":
    app.run()