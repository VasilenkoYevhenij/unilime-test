from flask import Flask
from flask_migrate import Migrate

from core.db import db
from api.views import views_bp
from api.services.parsing import products_and_reviews_parser
from core.cache import cache

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://ye_vasylenko:tp9jXSaEPWVwXUCqQ5h5MluL@localhost:5432/unilime"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False

db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

cache.init_app(app, config={"CACHE_TYPE": "SimpleCache"})

app.register_blueprint(views_bp)


@app.cli.command()
def parse():
    """Parsing files with products and reviews"""
    products_and_reviews_parser()


if __name__ == "__main__":
    app.run()
