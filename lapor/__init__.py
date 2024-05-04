from flask import Flask
from flask_cors import CORS
from .config.db import db
from .config.schema import ma

# routes
from .routes import review_route, auth_route, restaurant_route, user_route

# create the extension

# create the app
app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_route.bp)
app.register_blueprint(review_route.bp)
app.register_blueprint(restaurant_route.bp)
app.register_blueprint(user_route.bp)


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/food_review"

# initialize the app with the extension
db.init_app(app)
ma.init_app(app)
# @app.teardown_appcontext
# def close_db(err):
#     db.session.remove()


# def create_db():
#     with app.app_context():
#         db.create_all()


# if __name__ == "__main__":
#     create_db()
#     app.run(debug=True)
