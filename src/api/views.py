from flask import Blueprint, request, jsonify, make_response
from flask_paginate import get_page_parameter, get_per_page_parameter

from .models import ProductModel, ReviewModel
from api.services.reviews_pagination import paginated_reviews

from core.db import db
from core.cache import cache

views_bp = Blueprint("views", __name__)


@views_bp.route("/products/<int:product_id>/", methods=["GET"])
@cache.cached(timeout=50)
def product_detail_view(product_id):
    """Returns product details and list of reviews for current product"""

    product = ProductModel.query.get(product_id)
    if product:
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = request.args.get(get_per_page_parameter(), type=int, default=10)
        reviews = paginated_reviews(product_id, page, per_page)
        data = {"product": product.serialized_data, "reviews": reviews}
        return jsonify(
            data,
        )
    else:
        data = {"detail": "Not Found"}
        return make_response(jsonify(data), 404)


@views_bp.route("/products/<int:product_id>/", methods=["PUT"])
def add_product_review(product_id):
    """Add review for current product by id"""

    product = ProductModel.query.get(product_id)

    if product:
        review_data = request.get_json()
        title = review_data.get("title", None)
        review = review_data.get("review", None)
        if not title or not review:
            data = {"detail": '"review", "title" this fields are required'}
            return make_response(jsonify(data), 403)
        review_obj = ReviewModel(product.id, title, review)
        db.session.add(review_obj)
        db.session.commit()

        return make_response(jsonify(review_obj.serialized_data), 201)

    else:
        data = {"detail": "Not Found"}
        return make_response(jsonify(data), 404)
