from ..config.schema import ma
from ..models.Restaurant_model import Restaurant


class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant
        # include_fk = True


restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)
