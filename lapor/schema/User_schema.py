from ..config.schema import ma
from ..models.User_model import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

        fields = ("email", "user_name", "role_id")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
