from ..config.schema import ma
from ..models.Menu_model import Menu


class MenuSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Menu
        # include_fk = True


menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)
