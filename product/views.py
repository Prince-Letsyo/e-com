from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from helper.permissions import IsVerified
from product.models import (Product,ProductInventory, ProductCategory, 
                            ProductDiscount,ProductAd, Promotion)
from rest_framework.parsers import MultiPartParser, FormParser

from product.serializers import (ProductSerializer,ProductInventorySerializer,
                                 ProductCategorySerializer, ProductDiscountSerializer,
                                 ProductAdSerializer,PromotionSerializer)


class ProductListCreateAPIView(ListCreateAPIView):
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    permission_classes = (IsVerified,)
    

class ProductRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class=ProductSerializer
    permission_classes = (IsVerified,)
    queryset=Product.objects.all()
    lookup_field="id"
    
class ProductInventoryListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsVerified,)
    serializer_class=ProductInventorySerializer
    queryset=ProductInventory.objects.all()
    permission_classes = (IsVerified,)
    

class ProductInventoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class=ProductInventorySerializer
    queryset=ProductInventory.objects.all()
    permission_classes = (IsVerified,)
    lookup_field="id"
    
class ProductCategoryListCreateAPIView(ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class=ProductCategorySerializer
    queryset=ProductCategory.objects.all()
    permission_classes = (IsVerified,)
    

class ProductCategoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class=ProductCategorySerializer
    queryset=ProductCategory.objects.all()
    permission_classes = (IsVerified,)
    lookup_field="id"
    
class ProductDiscountListCreateAPIView(ListCreateAPIView):
    serializer_class=ProductDiscountSerializer
    queryset=ProductDiscount.objects.all()
    permission_classes = (IsVerified,)
    

class ProductDiscountRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class=ProductDiscountSerializer
    queryset=ProductDiscount.objects.all()
    permission_classes = (IsVerified,)
    lookup_field="id"
    
class PromotionListCreateAPIView(ListCreateAPIView):
    serializer_class=PromotionSerializer
    permission_classes = (IsVerified,)
    queryset=Promotion.objects.all()
    

class PromotionRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class=PromotionSerializer
    queryset=Promotion.objects.all()
    permission_classes = (IsVerified,)
    lookup_field="id"
    
class ProductAdListCreateAPIView(ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class=ProductAdSerializer
    permission_classes = (IsVerified,)
    queryset=ProductAd.objects.all()
    

class ProductAdRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsVerified,)
    serializer_class=ProductAdSerializer
    queryset=ProductAd.objects.all()
    lookup_field="id"
    