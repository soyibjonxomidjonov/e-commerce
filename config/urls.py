from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from billing.views import CreateChargeView


class JWTSchemaGenerator(OpenAPISchemaGenerator):

    def get_security_definitions(self):
        security_definitions = super().get_security_definitions()
        security_definitions['Bearer'] = {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
        return security_definitions


schema_view = get_schema_view(
    openapi.Info(
        title="API E-Commerce",
        default_version='v1',
        description='E-Commerce API',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="soyibjon12ss@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=JWTSchemaGenerator,
)

#  drf_yasg buni ikkinchi nomi >> swagger


# Bunday url bez-praktiska to'g'ri keladi
urlpatterns = [
    # Admin urliga ulash
    path('admin/', admin.site.urls),
    # productni urllariga ulash
    path("api/v1/", include("product.urls")),  # Bunday url bez-praktiska to'g'ri keladi
    path("api/v1/sms-auth/", include("custom_auth.urls")),

    # Urllarga Djoserni qo'shish uchun pastagi kodlar
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('api/v1/pay/', CreateChargeView.as_view(), name="create-charge"),

    # pastagi 3 qator kod hamma proyektlarga qo'shilishi shart

    # bu ham barcha proyektlarga qo'yib ketiladigan narsa
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ shu

    #  agar pustoy path() ga kirsa pastagi swaggerga kirib ketadi
    path('', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name="schema-redoc"),
]