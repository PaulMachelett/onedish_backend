from flask import request, jsonify
from onedish import app, db
from onedish.models import Users, Restaurant, Deal, UsedDeal, FavRestaurant
from onedish.schemas import *

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

# --- USERS ---
@app.route("/users", methods=["GET"])
def get_users():
    return users_schema.jsonify(Users.query.all())

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    return user_schema.jsonify(Users.query.get_or_404(id))

@app.route("/users", methods=["POST"])
def create_user():
    user = user_schema.load(request.json)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = Users.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# --- RESTAURANT ---
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    return restaurants_schema.jsonify(Restaurant.query.all())

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    return restaurant_schema.jsonify(Restaurant.query.get_or_404(id))

@app.route("/restaurants", methods=["POST"])
def create_restaurant():
    r = restaurant_schema.load(request.json)
    db.session.add(r)
    db.session.commit()
    return restaurant_schema.jsonify(r), 201

@app.route("/restaurants/<int:id>", methods=["PUT"])
def update_restaurant(id):
    r = Restaurant.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(r, key, value)
    db.session.commit()
    return restaurant_schema.jsonify(r)

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    r = Restaurant.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return '', 204

# --- DEALS ---
@app.route("/deals", methods=["GET"])
def get_deals():
    return deals_schema.jsonify(Deal.query.all())

@app.route("/deals/<int:id>", methods=["GET"])
def get_deal(id):
    return deal_schema.jsonify(Deal.query.get_or_404(id))

@app.route("/restaurants/<int:restaurant_id>/deals", methods=["GET"])
def get_deals_by_restaurant(restaurant_id):
    deals = Deal.query.filter_by(restaurant_id=restaurant_id).all()
    return deals_schema.jsonify(deals)

@app.route("/deals", methods=["POST"])
def create_deal():
    d = deal_schema.load(request.json)
    db.session.add(d)
    db.session.commit()
    return deal_schema.jsonify(d), 201

@app.route("/deals/<int:id>", methods=["PUT"])
def update_deal(id):
    d = Deal.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(d, key, value)
    db.session.commit()
    return deal_schema.jsonify(d)

@app.route("/deals/<int:id>", methods=["DELETE"])
def delete_deal(id):
    d = Deal.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return '', 204

# --- USED DEALS (user_id + deal_id als PK) ---
@app.route("/used_deals", methods=["GET"])
def get_used_deals():
    return used_deals_schema.jsonify(UsedDeal.query.all())

@app.route("/used_deals", methods=["POST"])
def create_used_deal():
    ud = used_deal_schema.load(request.json)
    db.session.add(ud)
    db.session.commit()
    return used_deal_schema.jsonify(ud), 201

@app.route("/used_deals/<int:user_id>/<int:deal_id>", methods=["DELETE"])
def delete_used_deal(user_id, deal_id):
    ud = UsedDeal.query.get_or_404((user_id, deal_id))
    db.session.delete(ud)
    db.session.commit()
    return '', 204

# --- FAVORITE RESTAURANTS (user_id + restaurant_id als PK) ---
@app.route("/fav_restaurants", methods=["GET"])
def get_fav_restaurants():
    return fav_restaurants_schema.jsonify(FavRestaurant.query.all())

@app.route("/fav_restaurants", methods=["POST"])
def create_fav_restaurant():
    fr = fav_restaurant_schema.load(request.json)
    db.session.add(fr)
    db.session.commit()
    return fav_restaurant_schema.jsonify(fr), 201

@app.route("/fav_restaurants/<int:user_id>/<int:restaurant_id>", methods=["DELETE"])
def delete_fav_restaurant(user_id, restaurant_id):
    fr = FavRestaurant.query.get_or_404((user_id, restaurant_id))
    db.session.delete(fr)
    db.session.commit()
    return '', 204