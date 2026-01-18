from rest_framework import viewsets
from product.models import Product
from product.permissons import IsStaffOrReadOnly
from rest_framework.pagination import PageNumberPagination
from product.serializers import ProductSerializers
from rest_framework.response import Response
from rest_framework import filters
from django_filters import rest_framework as django_filters
from product.filters import ProductFilter
from django.db import models
from rest_framework.decorators import action

# Agar shu yozilmasa settingsda belgilangan page size bo'yicha bo'ladi
class CustomPagination(PageNumberPagination):
    page_size = 3



# Pagination bunga qo'shildi!
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly] # Bu yerda faqat autentifikatsiyadan o'tgan foydalanuvchilar ko'ra oladi
    # Odatiy xolatda AllowAny turadi va hammaga ruhsat berib yuboradi
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    pagination_class = CustomPagination #Bunda pagination qo'shildi
    # Agar oddiy PageNumberPagination yozilsa settingsdagi page size bo'yicha bo'ladi

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']





# BUNDAN keyingi hamma funksiyalar CRUD  ni o'zgartiradigan funksiyalar list bu erkanga qanday chiqarishni o'zgartirish
    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category= instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializers(related_products, many=True)

        return Response(
            {
                'product': serializer.data,
                'related_products': related_serializer.data
            }
        )

    @action(detail=False, methods=["get"])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews_rating')).order_by("-avg_rating")[:2]
        serializer = ProductSerializers(top_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({"average_rating": "No reviews yet!"})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({"average_rating": avg_rating})
