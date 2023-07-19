from django.db import models
from product.models.product import Product
from user.models.utils import UserForeign


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews"
    )
    rating = models.IntegerField()
    desc = models.TextField()

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"


class UserReviewSession(UserForeign):
    review = models.OneToOneField(
        ProductReview, on_delete=models.CASCADE, related_name="user_review_sessions"
    )

    class Meta:
        verbose_name = "User Review Session"
        verbose_name_plural = "User Review Sessions"
