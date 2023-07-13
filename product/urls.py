from django.urls import path, re_path

from product.views import (ProductListCreateAPIView, ProductRetrieveUpdateAPIView,
                           ProductInventoryListCreateAPIView,ProductInventoryRetrieveUpdateAPIView,
                           ProductCategoryListCreateAPIView,ProductCategoryRetrieveUpdateAPIView,
                           ProductDiscountListCreateAPIView,ProductDiscountRetrieveUpdateAPIView,
                           ProductAdListCreateAPIView,ProductAdRetrieveUpdateAPIView,
                           PromotionListCreateAPIView,PromotionRetrieveUpdateAPIView
                           )


app_name="product"
urlpatterns = [
        path('', ProductListCreateAPIView.as_view(), name='product_list'),
        path('<int:id>/', ProductRetrieveUpdateAPIView.as_view(), name='product_detail'),
        path('inventory/', ProductInventoryListCreateAPIView.as_view(), name='inventory_list'),
        path('inventory/<int:id>/', ProductInventoryRetrieveUpdateAPIView.as_view(), name='inventory_detail'),
        path('category/', ProductCategoryListCreateAPIView.as_view(), name='category_list'),
        path('category/<int:id>/', ProductCategoryRetrieveUpdateAPIView.as_view(), name='category_detail'),
        path('discount/', ProductDiscountListCreateAPIView.as_view(), name='discount_list'),
        path('discount/<int:id>/', ProductDiscountRetrieveUpdateAPIView.as_view(), name='discount_detail'),
        path('ad/', ProductAdListCreateAPIView.as_view(), name='ad_list'),
        path('ad/<int:id>/', ProductAdRetrieveUpdateAPIView.as_view(), name='ad_detail'),
        path('promotion/', PromotionListCreateAPIView.as_view(), name='promotion_list'),
        path('promotion/<int:id>/', PromotionRetrieveUpdateAPIView.as_view(), name='promotion_detail'),
]