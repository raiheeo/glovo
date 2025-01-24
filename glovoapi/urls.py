from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title="Glove",
        default_version='v1',
        description="Site just created for fun!",
        contact=openapi.Contact(email="hayanomy.aki@gmail.com"),
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('glovo.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
