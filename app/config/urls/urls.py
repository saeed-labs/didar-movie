
from django.urls import path, include
from .v1 import urlpatterns  as v1_urlpatterns

from config.settings.conf import devlopment
from config.settings.conf import production


from django.conf.urls.static import static

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]




if production.DEBUG:
    urlpatterns += static(devlopment.MEDIA_URL, document_root=devlopment.MEDIA_ROOT)
    urlpatterns += static(devlopment.STATIC_URL,document_root=devlopment.STATIC_ROOT)