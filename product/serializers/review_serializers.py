from rest_framework import serializers
from helper.utils import writable_nested_serializer
from product.models.review import ProductReview, UserReviewSession


class UserReviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReviewSession

        fields = [
            "id",
            "user",
            "review",
        ]


class ProductReviewSerializer(serializers.ModelSerializer):
    user_review_sessions = UserReviewSessionSerializer(required=False)

    class Meta:
        model = ProductReview

        extra_fields = []

        if hasattr(model, "user_review_sessions"):
            extra_fields.append("user_review_sessions")

        fields = ["id", "product", "rating", "desc", *extra_fields]

    def to_internal_value(self, data):
        user_review_sessions = data.pop("user_review_sessions", None)

        if user_review_sessions:
            writable_nested_serializer(
                data=user_review_sessions,
                Modal=UserReviewSession,
                error=serializers.ValidationError(
                    {"user_review_sessions": "User review does not exist."}, 404
                ),
                Serializer=UserReviewSessionSerializer,
            )

        return super().to_internal_value(data)
