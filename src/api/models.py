from sqlalchemy.orm import relationship

from core.db import db


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    asin = db.Column(db.String(255), nullable=False)

    def __init__(self, title, asin):
        self.title = title
        self.asin = asin

    def __repr__(self):
        return f"<Product {self.asin}>"

    @property
    def serialized_data(self):
        data = {
            "id": self.id,
            "title": self.title,
            "asin": self.asin,
        }
        return data


class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    review = db.Column(db.Text, nullable=False)

    product = relationship("ProductModel", backref="reviews")

    def __init__(self, product_id, title, review):
        self.product_id = product_id
        self.title = title
        self.review = review

    def __repr__(self):
        return f"<{self.product.asin} {self.title}>"

    @property
    def serialized_data(self):
        data = {
            "id": self.id,
            "title": self.title,
            "review": self.review,
            "product": self.product_id,
        }
        return data
