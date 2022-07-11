from api.models import ReviewModel


def paginated_reviews(product_id, page, per_page) -> list:
    """Returns list of paginated and serialized reviews"""
    reviews = ReviewModel.query.filter_by(product_id=product_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    reviews_list = []
    if reviews:
        for review in reviews.items:
            reviews_list.append(review.serialized_data)
    return reviews_list
