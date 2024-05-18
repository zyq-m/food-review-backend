from ..config.schema import ma
from ..models.Review_model import Review


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        # include_fk = True


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
