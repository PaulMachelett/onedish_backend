from onedish import ma
from onedish.models import Users, Restaurant, Deal, UsedDeal, FavRestaurant

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True

class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant
        load_instance = True

class DealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Deal
        load_instance = True

class UsedDealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsedDeal
        load_instance = True

    user_id = ma.auto_field()
    deal_id = ma.auto_field()
    used_at = ma.auto_field()

class FavRestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavRestaurant
        load_instance = True