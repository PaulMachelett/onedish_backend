from onedish import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    sur_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=False)  # NEU
    password = db.Column(db.String(255), nullable=False)               # NEU (hashed)
    subscribed = db.Column(db.Boolean)
    google_id = db.Column(db.Integer)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    street = db.Column(db.String(255))
    street_number = db.Column(db.String(50))
    city = db.Column(db.String(255))
    zip_code = db.Column(db.Integer)
    cuisine = db.Column(db.Enum('asian', 'italian', 'german', 'greek', 'indian', 'mexican', 'american'))
    rating = db.Column(db.Float)
    open_hour = db.Column(db.Time)
    close_hour = db.Column(db.Time)
    website = db.Column(db.String(255))
    tel_number = db.Column(db.String(255))

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))
    price = db.Column(db.Float)
    saved_money = db.Column(db.Float)
    name = db.Column(db.String(255))
    description = db.Column(db.String(500))
    item_1 = db.Column(db.String(255))
    item_2 = db.Column(db.String(255))
    item_3 = db.Column(db.String(255))
    item_4 = db.Column(db.String(255))
    keyword_1 = db.Column(db.String(255))
    keyword_2 = db.Column(db.String(255))
    keyword_3 = db.Column(db.String(255))

class UsedDeal(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey("deal.id"), primary_key=True)
    used_at = db.Column(db.DateTime)

class FavRestaurant(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), primary_key=True)