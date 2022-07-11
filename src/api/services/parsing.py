import csv

from core.db import db
from api.models import ProductModel, ReviewModel


def products_and_reviews_parser() -> None:
    s = db.session()

    with open("files/reviews.csv", "r", encoding="utf8") as reviews_file, open(
        "files/products.csv", "r", encoding="utf8"
    ) as products_file:

        reviews = csv.reader(reviews_file, delimiter=",")
        products = csv.reader(products_file, delimiter=",")

        reviews_dict = dict()
        tmp_key = 0

        for review in reviews:  # collecting reviews into a dict
            if tmp_key == review[0]:
                sorted_reviews = reviews_dict[review[0]]
                sorted_reviews.append({"title": review[1], "review": review[2]})
            else:
                reviews_dict[review[0]] = [{"title": review[1], "review": review[2]}]
                tmp_key = review[0]

        objs_to_create = []

        for product in products:

            if product[1] == "Asin":
                continue

            asin = product[1]
            title = product[0]

            product_obj = ProductModel(title, asin)
            db.session.add(product_obj)
            db.session.flush()

            reviews_list_by_asin = reviews_dict.get(asin, None)

            if reviews_list_by_asin:
                for review in reviews_list_by_asin:
                    product_id = product_obj.id
                    objs_to_create.append(
                        ReviewModel(product_id, review["title"], review["review"])
                    )

        s.bulk_save_objects(objs_to_create)
        s.commit()
        print("Products and reviews were added successfully.")
