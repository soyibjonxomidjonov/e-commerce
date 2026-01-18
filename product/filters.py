from django_filters import rest_framework as django_filters  #pip install django-filter
from .models import Product, Review


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'name']




class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name']

class ReviewFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name="product__name", lookup_expr='icontains')

    class Meta:
        model = Review
        fields = ['product']

class FlashSaleFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name="product__name", lookup_expr='icontains')
    sale_range = django_filters.DateFromToRangeFilter(field_name='start_time')

    class Meta:
        model = Product
        fields = ['product']


