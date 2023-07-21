from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
)
from rest_framework.parsers import MultiPartParser, FormParser
from helper.permissions import IsVerified
from product.models import (
    Product,
    ProductInventory,
    ProductCategory,
    ProductDiscount,
    ProductAd,
    Promotion,
    CartItem,
)
from product.serializers import (
    ProductSerializer,
    ProductInventorySerializer,
    ProductCategorySerializer,
    ProductDiscountSerializer,
    ProductAdSerializer,
    PromotionSerializer,
    CartItemSerializer,
)

site_keys = [
    openapi.Parameter(
        name="Public-Key",
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        required=True,
    ),
    openapi.Parameter(
        name="Secret-Key",
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        required=True,
    ),
]


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsVerified,)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsVerified,)
    queryset = Product.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ProductInventoryListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsVerified,)
    serializer_class = ProductInventorySerializer
    queryset = ProductInventory.objects.all()

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductInventoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProductInventorySerializer
    queryset = ProductInventory.objects.all()
    permission_classes = (IsVerified,)
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ProductCategoryListCreateAPIView(ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    permission_classes = (IsVerified,)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductCategoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    permission_classes = (IsVerified,)
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ProductDiscountListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductDiscountSerializer
    queryset = ProductDiscount.objects.all()
    permission_classes = (IsVerified,)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductDiscountRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ProductDiscountSerializer
    queryset = ProductDiscount.objects.all()
    permission_classes = (IsVerified,)
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class PromotionListCreateAPIView(ListCreateAPIView):
    serializer_class = PromotionSerializer
    permission_classes = (IsVerified,)
    queryset = Promotion.objects.all()

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PromotionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PromotionSerializer
    queryset = Promotion.objects.all()
    permission_classes = (IsVerified,)
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductAdListCreateAPIView(ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductAdSerializer
    permission_classes = (IsVerified,)
    queryset = ProductAd.objects.all()

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductAdRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsVerified,)
    serializer_class = ProductAdSerializer
    queryset = ProductAd.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CartItemDestroyAPIView(DestroyAPIView):
    permission_classes = (IsVerified,)
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        manual_parameters=site_keys,
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
