from flask import request, jsonify
from onedish import app, db
from onedish.models import Users, Restaurant, Deal, UsedDeal, FavRestaurant
from onedish.schemas import *
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from onedish.schemas import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)

deal_schema = DealSchema()
deals_schema = DealSchema(many=True)

used_deal_schema = UsedDealSchema()
used_deals_schema = UsedDealSchema(many=True)

fav_restaurant_schema = FavRestaurantSchema()
fav_restaurants_schema = FavRestaurantSchema(many=True)


# --- REGISTER ---
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    # Pflichtfelder prüfen
    if not data.get("username") or not data.get("password") or not data.get("email"):
        return jsonify({"msg": "Benutzername, Passwort und E-Mail sind erforderlich"}), 400

    # Prüfen, ob Nutzername oder E-Mail bereits existieren
    if Users.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "Benutzername bereits vergeben"}), 409
    if Users.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "E-Mail bereits registriert"}), 409

    # Passwort hashen
    data["password"] = generate_password_hash(data["password"])

    # Benutzer speichern
    user = user_schema.load(data)
    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user), 201


# --- LOGIN ---
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = Users.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Login fehlgeschlagen"}), 401

# --- USERS ---
@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    return users_schema.jsonify(Users.query.all())

@app.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    return user_schema.jsonify(Users.query.get_or_404(id))

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    data["password"] = generate_password_hash(data["password"])
    user = user_schema.load(data)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@app.route("/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    user = Users.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204


# --- RESTAURANTS ---
@app.route("/restaurants", methods=["GET"])
@jwt_required()
def get_restaurants():
    return restaurants_schema.jsonify(Restaurant.query.all())

@app.route("/restaurants/<int:id>", methods=["GET"])
@jwt_required()
def get_restaurant(id):
    return restaurant_schema.jsonify(Restaurant.query.get_or_404(id))

@app.route("/restaurants", methods=["POST"])
@jwt_required()
def create_restaurant():
    r = restaurant_schema.load(request.json)
    db.session.add(r)
    db.session.commit()
    return restaurant_schema.jsonify(r), 201

@app.route("/restaurants/<int:id>", methods=["PUT"])
@jwt_required()
def update_restaurant(id):
    r = Restaurant.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(r, key, value)
    db.session.commit()
    return restaurant_schema.jsonify(r)

@app.route("/restaurants/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_restaurant(id):
    r = Restaurant.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return '', 204


# --- DEALS ---
@app.route("/deals", methods=["GET"])
@jwt_required()
def get_deals():
    return deals_schema.jsonify(Deal.query.all())

@app.route("/deals/<int:id>", methods=["GET"])
@jwt_required()
def get_deal(id):
    return deal_schema.jsonify(Deal.query.get_or_404(id))

@app.route("/restaurants/<int:restaurant_id>/deals", methods=["GET"])
@jwt_required()
def get_deals_by_restaurant(restaurant_id):
    deals = Deal.query.filter_by(restaurant_id=restaurant_id).all()
    return deals_schema.json_
