from flask import Blueprint
from src.routes.model.ranking_api import ranking_bp

api_blueprint = Blueprint("API", __name__, url_prefix="/api/")
api_blueprint.register_blueprint(ranking_bp)


@api_blueprint.route("/", methods=["GET"])
def get_data():
    return "Homepage route setup!"
