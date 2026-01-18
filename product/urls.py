from . import signals
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .services.flash_sale import check_flash_sale
from .services.product_view_history import ProductViewHistoryCreate
from .services.replenish_stock import admin_replenish_stock
from .views import ProductViewSet, ReviewViewSet, CategoryViewSet, product_list, ProductListCreate, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
#     Agar view funksiya bilan yozilgan bo'lsa  product_list() - bunda () lar yozilmaydi
    path("products_list_funk/", product_list, name="product_list"),

#     Agar view class bilan yozilgan bo'lsa classni oxiriga as_view() qo'shib qo'yiladi
#     Ya'ni class basedlarda .as_view() qo'shiladi
    path("products_list_class/", ProductListCreate.as_view(), name="products_list_class"),
    path('check-sale/<int:product_id>/', check_flash_sale, name='product-view-history-create'),
    path('product-view/', ProductViewHistoryCreate.as_view(), name='product-view-history-create'),
    path('admin/replenish_stock/<int:product_id>/<int:amount>/', admin_replenish_stock, name='admin_replenish_stock'),

]