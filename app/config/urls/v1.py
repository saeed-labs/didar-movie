from django.urls import path, include
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('user/', include('accounts.urls')),
]


urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
