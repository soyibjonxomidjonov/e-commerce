from drf_yasg.openapi import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from product.models import Review, Category, Order, Product
from product.permissons import IsOwnerOrReadOnly, IsStaffOrReadOnly
from product.serializers import OrderSerializer, ProductSerializers
from product.serializers import ReviewSerializers, CategorySerializers
from rest_framework import viewsets, filters, generics


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializers



class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

class ProductListCreate(generics.ListCreateAPIView): #Bunda generic view bo'ladi
    permission_classes = [IsStaffOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
#  Bunda list va create metodi bor qolganlari yo'q ya'ni CRUD  emas

# Agar oddiy funksiya bilan ham view yozish kerak bo'lsa >> api_view decoratori ishlatiladi

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication]) # bunda belgilab qoyildi
@permission_classes([IsAuthenticated]) # Bunda permison qoshildi
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializers(products, many=True)
    return Response(serializer.data)


# Agar tepadiagidaqa qilib funskyisani ichida view yozilsa urllarga ham ma'lumot qo'shish talab qilinadi


