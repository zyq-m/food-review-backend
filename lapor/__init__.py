from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from .config.db import db
from .config.schema import ma
from .config.jwt import jwt

# routes
from .routes import review_route, auth_route, restaurant_route, user_route

# create the app
app = Flask(__name__)

CORS(app)

app.register_blueprint(auth_route.bp)
app.register_blueprint(review_route.bp)
app.register_blueprint(restaurant_route.bp)
app.register_blueprint(user_route.bp)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/food_review"
app.config["SECRET_KEY"] = "your_strong_secret_key"
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# initialize the app with the extension
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)
