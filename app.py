from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import pyrebase
import requests
import os
app = Flask(__name__)
app.config["DEBUG"] = True
config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": "authdemo-696ae.firebaseapp.com",
    "databaseURL": "https://authdemo-696ae.firebaseio.com",
    "storageBucket": "authdemo-696ae.appspot.com"
}
firebase = pyrebase.initialize_app(config)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")  # Change this!
jwt = JWTManager(app)
# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    # Get a reference to the auth service
    auth = firebase.auth()

    # Log the user in
    try:
        user = auth.sign_in_with_email_and_password(username, password)
    except requests.exceptions.HTTPError:
        return jsonify({"msg": "Wrong Username or password"}), 400

    # create tokens
    id = user['localId']
    access_token = create_access_token(identity=id)
    refresh_token = create_refresh_token(identity=id)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token, "msg": user}), 200


@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World</h1>"


# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()

    access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": access_token}), 200

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/books', methods=['GET'])
@jwt_required
def api_all():
    return jsonify(books)


app.run()
